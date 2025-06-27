# **GP Time Offset Duplicator**

**GP Time Offset Duplicator** lets you temporarily step out of the timeline controlled by the Time Offset modifier—either duplicating the displayed frame or creating a blank keyframe—so you can create a new drawing without altering the ongoing keyframed animation.

- **Target an Existing Layer or Create a New One:**  
  You can choose whether to:

  - **Duplicate the new keyframe on an existing layer,** placing the new drawing right where you want it, or
  - **Create a new layer** specifically to hold the duplicated (or blank) keyframe, keeping your drawings neatly separated.

- **Duplicate or Create a Blank Keyframe:**  
  The operator offers two modes:

  - **Duplicate the Active Frame:**  
    It copies the frame currently referenced by the Time Offset modifier, preserving its drawing data as a starting point.
  - **Create a Blank Keyframe:**  
    Alternatively, you can opt to start with a clean slate. In this case, the operator creates a blank keyframe either on the destination layer or—if desired—on the original layer to hide its content. This ensures that the Grease Pencil only shows your new drawing.

- **Quick Re-enable:**  
  After your new drawing is complete, you can easily re-enable the Time Offset modifier directly from the Dopesheet's Header. This lets you seamlessly return to the keyframed animation with your fresh adjustments integrated.

By offering these options, **GP Time Offset Duplicator** provides a flexible, non-destructive workflow that adapts to your creative needs.

## Features

- **Jump Out of Timeline**: Temporarily exit the timeline controlled by the Time Offset modifier to create a new drawing without affecting the keyframed animation.
- **Duplicate with Ease**: Quickly duplicate the active Grease Pencil frame influenced by the Time Offset modifier—or create a blank keyframe—so you have a new, editable drawing surface.
- **Quick Re-enable**: Easily re-enable the Time Offset modifier directly from the Dopesheet's Header once your new drawing is complete.
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
zip -r "GP_Time_Offset_Duplicator_v1.0.0.zip" *
mv "GP_Time_Offset_Duplicator_v1.0.0.zip" ~/Downloads/
```

This will:

- Create a tag (e.g. `v1.0.0`) marking the current commit as a release.
- Push the tag to GitHub so that it appears in the Releases section.
- Package all repository files into a zip file named `GP Time Offset Duplicator_v1.0.0.zip` for users to download.
- Move the generated zip file to your Downloads folder.

### Video Tutorial

For a quick overview and demonstration of the add-on in action, watch the video below:

<div align="center">
  <video width="560" height="315" controls>
    <source src="Grease Pencil Time Offset Duplicator.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</div>
