import os
import sys
import shutil
import pathlib
from shutil import copy2
from packaging import version

# Change the working directory to the directory of this script
script_directory = pathlib.Path(__file__).parent.absolute()
os.chdir(script_directory)


def get_blender_data_path() -> pathlib.Path:
    home = pathlib.Path.home()
    if sys.platform == "win32":
        return os.path.join(home, "AppData", "Roaming", "Blender Foundation", "Blender")
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return os.path.join(home, "Library", "Application Support", "Blender")


def check_path(path):
    if os.path.exists(path):
        print(f"Folder: {path}")
        return True
    else:
        print(f"Sorry, but the path {path} does not exist.")
        return False


def get_installations(directory):
    subds = []
    add_ons_paths = []

    try:
        subds = [
            name
            for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))
        ]
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")
        return []

    print(f"Subdirectories found in {directory}: {subds}")

    for subd in subds:
        try:
            parsed_version = version.parse(subd)
            is_version = isinstance(parsed_version, version.Version)
            print(
                f"Checking {subd}: Parsed version {parsed_version}, Valid: {is_version}"
            )
        except Exception as e:
            print(f"Skipping {subd}, not a valid version. Error: {e}")
            continue

        if is_version:
            if parsed_version >= version.parse("4.2"):
                add_ons_path = os.path.join(
                    directory, subd, "extensions", "user_default"
                )
            else:
                add_ons_path = os.path.join(directory, subd, "scripts", "addons")

            if os.path.isdir(add_ons_path):
                print(f"Valid installation found: {add_ons_path}")
                add_ons_paths.append(add_ons_path)
            else:
                print(f"No valid addons path found for {subd}")

    return add_ons_paths


def increment_version(current_version):
    major, minor, patch = current_version
    patch += 1
    if patch > 99:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1
    return major, minor, patch


def update_bl_info_version(init_file, new_version):
    with open(init_file, "r") as f:
        lines = f.readlines()

    with open(init_file, "w") as f:
        for line in lines:
            if line.startswith('    "version": '):
                # Keep them as integers in __init__.py, no need for zero-padding here
                f.write(
                    f'    "version": ({new_version[0]}, {new_version[1]}, {new_version[2]}),\n'
                )
            else:
                f.write(line)


def update_manifest_version(manifest_file, new_version):
    with open(manifest_file, "r") as f:
        lines = f.readlines()

    with open(manifest_file, "w") as f:
        for line in lines:
            if line.startswith("version = "):
                # Zero-pad the patch number
                f.write(
                    f'version = "{new_version[0]}.{new_version[1]}.{new_version[2]}"\n'
                )
            else:
                f.write(line)


# In our repository the add-on folder is "GP Time Offset Duplicator"
dist_folders = ["GP Time Offset Duplicator"]

add_on_directories = []

if check_path(get_blender_data_path()):
    print("get_blender_data_path", get_blender_data_path())
    add_on_directories = get_installations(get_blender_data_path())
    for i, d in enumerate(add_on_directories):
        print(i, d)

for dist in dist_folders:
    path = pathlib.Path(__file__).parent.resolve()
    # The distribution folder for the zip archive
    dist_folder = os.path.join(path, f"{dist}_dist")

    # Clear the dist folder
    for filename in os.listdir(dist_folder):
        file_path = os.path.join(dist_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    # Use the add-on folder itself as the source for the ZIP
    zip_dir = os.path.join(path, dist)
    zip_target_dir = zip_dir  # our source folder for the archive
    init_path = os.path.join(zip_dir, "__init__.py")
    manifest_path = os.path.join(zip_dir, "blender_manifest.toml")

    # Get current version from __init__.py in the add-on folder
    current_version = (1, 0, 0)
    with open(init_path) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('    "version": '):
                try:
                    ver = eval(line.partition(": ")[-1].strip().strip(","))
                    if isinstance(ver, (tuple, list)) and len(ver) == 3:
                        current_version = tuple(ver)
                    else:
                        # Try converting to a version tuple from a string or single value.
                        parts = str(ver).split(".")
                        if len(parts) < 3:
                            parts += ["0"] * (3 - len(parts))
                        current_version = tuple(map(int, parts[:3]))
                except Exception as e:
                    print(
                        f"Failed to parse version from __init__.py; defaulting to (1, 0, 0). Error: {e}"
                    )
                    current_version = (1, 0, 0)
                break

    # Increment the patch version
    new_version = increment_version(current_version)

    # Update the version in __init__.py
    update_bl_info_version(init_path, new_version)

    # Update the version in blender_manifest.toml
    if os.path.exists(manifest_path):
        update_manifest_version(manifest_path, new_version)

    # Create a version string (patch is not zero-padded in __init__)
    version_str = f"_v{new_version[0]}.{new_version[1]}.{new_version[2]}"
    filename = f"{dist}{version_str}"
    destination = os.path.join(dist_folder, filename)
    # Create the zip archive from the add-on folder
    shutil.make_archive(destination, "zip", root_dir=zip_dir)

    for blender_addons_path in add_on_directories:
        print(f"Checking path: {blender_addons_path}")
        dist_addon_path = os.path.join(blender_addons_path, dist)

        if "extensions/user_default" in blender_addons_path:
            modified_dist = dist.lower().replace(" ", "_")
        else:
            modified_dist = dist

        print("Existing dirs in path:", os.listdir(os.path.dirname(dist_addon_path)))
        dist_addon_path = os.path.join(blender_addons_path, modified_dist)

        print(f"addon_path: {dist_addon_path}")

        print("\n=== DEBUG INFO ===")
        print(f"dist: {dist}")
        print(f"modified_dist: {modified_dist}")
        print(f"blender_addons_path: {blender_addons_path}")
        print(f"dist_addon_path: {dist_addon_path}")
        print("==================")

        print(f"Attempting to delete: {dist_addon_path}")
        if os.path.exists(dist_addon_path) and os.path.isdir(dist_addon_path):
            try:
                shutil.rmtree(dist_addon_path)
            except Exception as e:
                print(f"Failed to delete {dist_addon_path}: {e}")
            print(f"Deleted: {dist_addon_path}")
        else:
            print(f"Could not find: {dist_addon_path}")

        shutil.copytree(
            zip_dir,
            dist_addon_path,
            symlinks=False,
            ignore=None,
            copy_function=copy2,
            ignore_dangling_symlinks=False,
            dirs_exist_ok=False,
        )

        print(f"filename: {filename}.zip")
        print(f"destination: {destination}.zip")
        print(f"zip_dir: {zip_dir}")
