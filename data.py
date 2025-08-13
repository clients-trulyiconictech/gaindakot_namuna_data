import os
import json

# Define media types
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
all_media_extensions = image_extensions + video_extensions

# Define directories
output_dir = 'database'
media_dir = 'media'
others_dir = 'others'
notice_dir = 'notice'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# Process media directory (images)
# -----------------------------
media_json_path = os.path.join(output_dir, 'media.json')
image_files_by_folder = {}

if os.path.isdir(media_dir):
    for subfolder in sorted(os.listdir(media_dir), reverse=True):
        subfolder_path = os.path.join(media_dir, subfolder)
        if os.path.isdir(subfolder_path):
            images = []
            for file in sorted(os.listdir(subfolder_path), reverse=True):
                file_path = os.path.join(subfolder_path, file)
                if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
                    relative_path = os.path.join(media_dir, subfolder, file).replace('\\', '/')
                    images.append(relative_path)
            if images:
                image_files_by_folder[subfolder] = images

    # Reverse the folder order
    reversed_images = dict(reversed(image_files_by_folder.items()))
    with open(media_json_path, 'w') as f:
        json.dump({"images": reversed_images}, f, indent=4)

# -----------------------------
# Process others directory (videos or other media)
# -----------------------------
others_json_path = os.path.join(output_dir, 'others.json')
others_dict = {}

if os.path.isdir(others_dir):
    for file in sorted(os.listdir(others_dir), reverse=True):
        file_path = os.path.join(others_dir, file)
        name, ext = os.path.splitext(file)
        if os.path.isfile(file_path) and ext.lower() in all_media_extensions:
            key = name
            value = os.path.join('others', file).replace('\\', '/')
            others_dict[key] = value

    # Reverse to have latest files first
    reversed_others = dict(reversed(others_dict.items()))
    with open(others_json_path, 'w') as f:
        json.dump(reversed_others, f, indent=4)

# -----------------------------
# Process notices
# -----------------------------
notice_json_path = os.path.join(output_dir, 'notice.json')
notices = []

if os.path.isdir(notice_dir):
    for folder_name in sorted(os.listdir(notice_dir), reverse=True):
        folder_path = os.path.join(notice_dir, folder_name)
        if os.path.isdir(folder_path) and '-' in folder_name:
            try:
                date_part, title_part = folder_name.split('-', 1)
                formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"
                raw_title = title_part.replace('_', ' ').strip()
                title_formatted = raw_title
                title_title_case = raw_title.title()

                file_entries = []
                for file in sorted(os.listdir(folder_path), reverse=True):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        ext = os.path.splitext(file)[1].lstrip('.').lower()
                        relative_path = os.path.join('notice', folder_name, file).replace('\\', '/')
                        file_entries.append({
                            "file_name": title_title_case,
                            "file_type": ext,
                            "file_path": relative_path
                        })

                if file_entries:
                    notice = {
                        "id": title_formatted.replace(" ", "-"),
                        "date": formatted_date,
                        "title": title_formatted,
                        "files": file_entries
                    }
                    notices.append(notice)
            except Exception as e:
                print(f"Error processing notice folder '{folder_name}': {e}")

# Reverse the notices list so newest ones come first
with open(notice_json_path, 'w', encoding='utf-8') as f:
    json.dump({"notices": list(notices)}, f, indent=4)

# -----------------------------
# Update version
# -----------------------------
version_file = os.path.join(output_dir, 'version.json')

if os.path.exists(version_file):
    with open(version_file, 'r') as vf:
        version_data = json.load(vf)
    version = version_data.get("version", 0) + 1
else:
    version = 0

with open(version_file, 'w') as vf:
    json.dump({"version": version}, vf, indent=4)
