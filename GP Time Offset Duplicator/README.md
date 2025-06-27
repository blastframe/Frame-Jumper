# GP Time Offset Duplicator

GP Time Offset Duplicator is a Blender add-on designed to duplicate the active Grease Pencil frame that is affected by the Time Offset modifier into a new, editable frame. This non-destructive workflow allows you to preserve the original animation while making precise edits to the duplicated frame.

## Features

- **Duplicate with Ease**: Quickly duplicate an active Grease Pencil frame influenced by a Time Offset modifier.
- **Non-Destructive Editing**: Work on a duplicated frame without altering the original animation.
- **Compatibility**: Designed to work with both Grease Pencil v2 and v3 workflows.

## Installation

Follow these steps to install the GP Time Offset Duplicator add-on in Blender:

1. **Download the Add-on:**

   - Clone or download this repository from GitHub.

   ```bash
   git clone https://github.com/yourusername/GP-Time-Offset-Duplicator.git
   ```

2. **Install via Blender Preferences:**

   - Open Blender.
   - Go to **Edit > Preferences > Add-ons**.
   - Click on the **Install…** button.
   - Navigate to the downloaded repository folder and select the `zip` file or the folder containing the add-on.
   - Enable the add-on by checking the box next to its name.

3. **Verify Installation:**
   - The add-on should now be visible under the **3D Viewport > Sidebar > GP Time Offset Tools** panel.

## How to Use

### Step-by-Step Guide

1. **Setup Your Grease Pencil Object:**

   - Create or select an existing Grease Pencil object in your scene.
   - Apply a Time Offset modifier if required.

2. **Activate the Frame:**

   - In the Grease Pencil timeline or on the canvas, choose the frame you wish to duplicate.

3. **Duplicate the Frame:**

   - Open the sidebar (Press `N` in the 3D Viewport) and navigate to the **GP Time Offset Tools** tab.
   - Click on the **Duplicate Frame** button.
   - The add-on will duplicate the active frame (while copying ease data, handle angles, and interpolation settings) into a new frame for editing.

4. **Edit the Duplicated Frame:**

   - The duplicated frame will appear in the timeline as a separate frame.
   - Edit the new frame as desired without affecting the original frame.

5. **Saving Your Work:**
   - Once satisfied, save your Blender file. The add-on does not automatically commit changes, so manual saving is required.

## Troubleshooting

- **Add-on Not Appearing:**  
  Double-check that the installation was completed correctly (via Blender Preferences > Add-ons). Also, verify that you’re using a compatible version of Blender.

## License

This add-on is released under the [MIT License](LICENSE).

## Contributing

Contributions, suggestions, and fixes are welcome! Feel free to fork this repository and submit pull requests.

## Acknowledgements

- Special acknowledgement to [**Joel at SketchySquirrel**](https://www.youtube.com/c/SketchySquirrel) for the inspiration and idea behind this add-on, as well as for providing invaluable rigging insights to the Grease Pencil user base.
- IG: @sketchysquirrelanimation
- For more details and projects, visit his [GitHub](https://github.com/sketchy-squirrel) repository.
- Inspired by the need for flexible Grease Pencil editing tools.

---

Happy Grease Penciling!
