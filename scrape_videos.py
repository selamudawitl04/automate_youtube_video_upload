import instaloader
import os
import config
from datetime import datetime, timedelta

def remove_session(username):
    session_file = os.path.expanduser(f"~/.config/instaloader/session-{username}")
    if os.path.exists(session_file):
        os.remove(session_file)
        print(f"Removed session file for username: {username}")
    else:
        print(f"No session file found for username: {username}")

def download_instagram_videos(username, password, output_folder, days=7, max_videos=5):
    L = instaloader.Instaloader(dirname_pattern=output_folder)
    total_downloaded = 0  # Counter for total downloaded videos

    try:
        if username:
            session_file = os.path.expanduser(f"~/.config/instaloader/session-{username}")

            try:
                L.load_session_from_file(username, filename=session_file)  # Load session for authenticated access
            except FileNotFoundError:
                print("Session file not found. Attempting to log in.")
                L.context.log("Session file does not exist, logging in.")
                L.login(username, password)
                L.save_session_to_file(filename=session_file)

            profile = instaloader.Profile.from_username(L.context, username)

            print(f"Profile: {profile.username}")

            followees = profile.get_followees()

            # Count followees manually
            followee_count = sum(1 for _ in followees)
            print(f"Downloading videos from {followee_count} followees.")

            # Reset the iterator
            followees = profile.get_followees()

            # Calculate the date threshold
            date_threshold = datetime.now() - timedelta(days=days)

            for followee in followees:
                profile_name = followee.username
                print(f"Processing profile: {profile_name}")
                profile = instaloader.Profile.from_username(L.context, profile_name)
                count = 0
                found_videos = False
                for post in profile.get_posts():
                    # Filter posts by date
                    if post.is_video and post.date_utc >= date_threshold:
                        L.download_post(post, target=profile_name)
                        count += 1
                        found_videos = True
                        total_downloaded += 1  # Increment the total downloaded counter
                        if count >= max_videos:
                            break
                if not found_videos:
                    print(f"No videos found on the profile '{profile_name}' within the last {days} days.")
        else:
            print("Please set the environment variable INSTAGRAM_USERNAME.")
    except instaloader.exceptions.LoginRequiredException:
        print("Login required, but session file or credentials are missing.")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        print("Two-factor authentication is required. Please complete it in the Instaloader CLI and try again.")
    except instaloader.exceptions.InstaloaderException as e:
        print(f"An error occurred: {e}")

    print(f"Total videos downloaded: {total_downloaded}")

if __name__ == "__main__":
    download_instagram_videos('', '', "new-test-video", days=5)
