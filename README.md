# **GP Time Offset Duplicator**

---

### What is the GP Time Offset Duplicator?

Sometimes, while you're using that Time Offset modifier, you might want to draw something _new_ without messing up the awesome rigged animation you've already set up with a Time Offset Modifier. That's where the **GP Time Offset Duplicator** comes in!

Think of it like this: The Time Offset modifier is showing you a specific drawing from your animation. The **GP Time Offset Duplicator** lets you "step out" of that view for a moment. You can either make a copy of the drawing you see or create a completely blank canvas, and then draw something brand new without changing your existing animation. How cool is that?

---

### Where Can Your New Drawing Go?

When you use this tool, you have a choice about where your new drawing will appear:

- **Put it on an existing layer:** If you want your new drawing to be part of a layer you're already working on, you can do that! It will pop right into that layer.
- **Create a brand new layer:** Sometimes, it's nice to keep your drawings super organized. This option lets you make a fresh, empty layer just for your new drawing. This keeps everything neat and tidy!

---

### Do You Want a Copy or a Clean Slate?

The **GP Time Offset Duplicator** gives you two ways to start your new drawing:

- **Duplicate the current drawing:** This is like taking a photocopy of the drawing the Time Offset modifier is currently showing you. You'll get an exact copy, and you can then draw on top of it or change it however you like. It's a great way to start if you want to build upon something already there.
- **Create a blank drawing:** If you want to start completely from scratch, this is your option! It will give you an empty space to draw on. You can even choose to make the original drawing (the one the Time Offset modifier was showing) temporarily disappear so only your new drawing is visible. This makes sure you can focus entirely on your new creation.

---

### Getting Back to Your Animation

Once you're done with your new drawing, don't worry! It's super easy to go back to your regular animation controlled by the Time Offset modifier. There's a quick button in the **Dopesheet's Header** (which is a part of Blender where you manage your animation frames) that lets you turn the Time Offset modifier back on. Then, your new drawing will fit perfectly into your ongoing animation!

### Video Tutorial

For a quick demonstration of the add-on in action, watch the video below:
[![Grease Pencil Time Offset Duplicator](https://img.youtube.com/vi/TUGGjXJURmU/0.jpg)](https://www.youtube.com/watch?v=TUGGjXJURmU)

By offering these options, **GP Time Offset Duplicator** provides a flexible, non-destructive workflow that adapts to your creative needs.

**Compatibility**: Designed to work with both Grease Pencil v2 and v3 workflows.

## Installation

To install the **GP Time Offset Duplicator** add-on from the released zip file, follow these steps:

## Installing **GP Time Offset Duplicator** in Blender 4.x via the _Extensions_ panel (ZIP workflow)

> **Heads-up:** Blender 4 introduced the _Extensions_ manager, but you can still install any ZIP-based add-on/extension locally. These steps assume you already downloaded `GP_Time_Offset_Duplicator_vX.Y.Z.zip`.

1. **Open Preferences → Extensions**

   - In Blender’s top-bar choose **Edit ▸ Preferences…**.
   - Click the **Extensions** tab in the sidebar.

2. **Switch to “Get Extensions”** (top of the window).

   - This page lists the on-line catalog, but it also hides the local install option we need.

3. **Install from Disk**

   1. Press the Down Arrow menu in the top-right corner and pick **Install from Disk…**  
      _Alternatively, drag-and-drop the ZIP onto the Extensions window._
   2. In the file browser, locate and select `GP_Time_Offset_Duplicator_vX.Y.Z.zip`.
   3. Click **Install Extension**. Blender copies the files into your _Local Repository_.

4. **Enable the Add-on**

   - Still in Preferences ▶ Add-ons, go to the **Installed** tab.
   - Tick the checkbox next to **GP Time Offset Duplicator** to load it.

5. **Close Preferences**
   - The tool now appears in the Dope-Sheet header, ready to duplicate Time-Offset frames.

### Notes

- Installing from a ZIP adds the extension **locally**; it won’t auto-update thru the on-line catalog.
- If you later need to remove it, return to **Installed**, click the Down Arrow next to the name, and choose **Remove**.
- For legacy 3.x add-ons that lack an `extension_manifest.json`, use **Add-ons ▸ Install from Disk…** instead.

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
