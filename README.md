# **GP Time Offset Duplicator**

**GP Time Offset Duplicator** is a Blender add-on designed to duplicate the active Grease Pencil frame that is affected by the Time Offset modifier into a new, editable frame. This non-destructive workflow allows you to preserve the original animation while making precise edits to the duplicated frame.

## Features

- **Duplicate with Ease**: Quickly duplicate an active Grease Pencil frame influenced by a Time Offset modifier.
- **Non-Destructive Editing**: Work on a duplicated frame without altering the original animation.
- **Compatibility**: Designed to work with both Grease Pencil v2 and v3 workflows.

## Installation

To install the **GP Time Offset Duplicator** add-on from the released zip file, follow these steps:

1. **Download the Add-on Package:**

   - Go to the [Releases](https://github.com/blastframe/GP-Time-Offset-Duplicator/releases) page of this repository.
   - Download the latest `GP Time Offset Duplicator_vX.Y.Z.zip` file.

2. **Open Blender Preferences:**

   - Open Blender.
   - From the main Blender menu, click on **Edit** and then select **Preferences**.

3. **Navigate to the Add-ons Tab:**

   - In the Preferences window, click on the **Add-ons** tab.

4. **Initiate Installation:**

   - At the top right of the Add-ons panel, click the **Install...** button.

5. **Locate the Zip File:**

   - A file browser window will open.
   - Navigate to the location on your computer where you saved the downloaded zip file.

6. **Select and Install:**

   - Select the zip file and click the **Install Add-on** button in the file browser.

7. **Enable the Add-on:**
   - Once installed, the add-on will appear in the list.
   - Enable it by clicking the checkbox next to **GP Time Offset Duplicator**.

You are now ready to use the add-on from the **3D Viewport > Sidebar > GP Time Offset Tools** panel.

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
- For more details and projects, visit Joel's [GitHub](https://github.com/sketchy-squirrel) repository.
- Inspired by the need for flexible Grease Pencil editing tools.

---
