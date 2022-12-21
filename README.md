# BatchMDL

BatchMDL is a Blender addon for exporting groups of static props to Source Engine.

## Usage

### Games

Before you can export anything, you'll need to setup a game.

![Games](./docs/games.png)

A game consists of a name and 5 paths.

- **Game**: The folder containing `gameinfo.txt`; setting this will auto fill the other paths
- **Compiler**: The program `studiomdl.exe`, which should be in your game's `bin` folder
- **Viewer**: The program `hlmv.exe`, which should also be in your game's `bin` folder
- **Source**: The folder for QC and SMD/FBX files, typically `modelsrc`
- **Target**: The folder for MDL files, typically `models`

You may want to use a subfolder of `steamapps/common` as Source path if you plan on using
[static prop combine](https://developer.valvesoftware.com/wiki/Static_Prop_Combine).

### Export

This addon requires a specific collection structure and naming convention.

![Export](./docs/export.png)

At the top there's the root collection, it contains group collections.
Group collections in turn contain model collections.
Model collections contain objects and collections that are exported.

The name of a model is the name of its group and model collections, with a slash in between.
Meaning a group collection named `A`, plus a model collection named `B`, will result in a model with the name `A/B`.
Exported files are made lowercase and have certain characters replaced with underscores for compatibility.

All objects and collections inside a model collection are exported into two files.
Reference and collision, which is determined by the object or collection name.
Names of objects inside sub collections don't matter, only items in the model collection.
The reference mesh is visible, while the collision mesh is tangible.

If the name of an object or collection ends with `col`, `collision`, `phys`, or `physics`,
it is used as collision; otherwise it is used as reference.
An object whose name ends with `orig` or `origin` will be used as origin,
meaning all objects in the model collection will be relative to it in the exported model.
Collision and origin are both optional, reference is not.

In the screenshot above, various collection structures and naming conventions are shown;
these are all valid, and can be mixed.
Sub collections can contain multiple objects.
All object types that can be converted to mesh should work.

In the panel, groups and models are listed, and have a few options.
The checkbox determines whether a group or model is exported.
Which group and model are selected determine what the View button does.
If an option is set on a model, it overrides the value from the group.

- **Surface Property**: What the model is made of, this affects sounds and decals
- **Material Folder**: Where to look for VMT files, relative to the game's `materials` folder

## Links

- Join the [Discord](https://discord.com/invite/N35zhHm) server
- Buy my other addons on [Gumroad](https://bonjorno7.gumroad.com) or [BlenderMarket](https://blendermarket.com/creators/bonjorno7)
- Donate on [PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=43R2CKWLJZ78S)
