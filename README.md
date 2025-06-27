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

1. **Setup Your Scene:**

   - Ensure your Grease Pencil object is in the scene.
   - Apply a Time Offset modifier to the object. This modifier (driven by keyframes) controls which frame is displayed during playback.

2. **Preparing for a New Drawn Frame:**

   - When you reach a point in the animation where you need a newly drawn frame, open the sidebar (press `N` in the 3D Viewport) and navigate to the **GP Time Offset Tools** tab.
   - Click the **Duplicate Time Offset Frame** button which shows as a Time Modifier icon in the header of the Dopesheet Editor. This operator will disable the active Grease Pencil object's Time Offset modifier and duplicate the currently displayed frame (the one being driven by keyframes) into a new frame.
   - Additionally, if enabled, it can create a blank keyframe on the source layer so that the original drawing does not show underneath.

3. **Drawing the New Frame:**

   - With the modifier now temporarily disabled, switch to Draw mode and create your new artwork on the duplicated frame.
   - The new frame is independent—allowing you to make changes without affecting the original keyframed animation.

4. **Re-enable the Time Offset Modifier:**
   - Once you’re satisfied with your new frame, re-enable the Time Offset modifier (for example, by using the viewport toggle button provided by the add-on).
   - Your animation will now resume its keyframed control, but with the new frame integrated into the sequence.

By following these steps, you efficiently use **GP Time Offset Duplicator** to integrate hand-drawn modifications into your animated Grease Pencil layers.

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

### Tagging and Packaging a Release

To create a new release, follow these steps in your repository's root:

```bash
git tag v1.0.0
git push --tags
zip -r "GP Time Offset Duplicator_v1.0.0.zip" *
mv "GP Time Offset Duplicator_v1.0.0.zip" ~/Downloads/
```

This will:

- Create a tag (e.g. `v1.0.0`) marking the current commit as a release.
- Push the tag to GitHub so that it appears in the Releases section.
- Package all repository files into a zip file named `GP Time Offset Duplicator_v1.0.0.zip` for users to download.
- Move the generated zip file to your Downloads folder.
