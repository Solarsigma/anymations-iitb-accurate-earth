# Accurate Earth

## Instructions for usage:
Run it from the command line as follows:  
`blender --background --python combined.py -- [options]`  
Following flags (options) are available:  
- `--time` or `-t`: Time of day passed in the format of `HH:mm` where HH and mm are 1-indexed integers of the hour of day and minute of day respectively. Default is set to current time.
- `--date` or `-d`: Date passed in the format `YYYY-MM-DD` where YYYY is the year, MM is the month, DD is the date (all 1-indexed integers). Default is set to current date.
- `--save` or `-s`: Pass this flag if you want to save the blend file.
- `--animate` or `-a`: Pass this flag if you want the scene to be animated (both clouds and the camera)
- `--latitude` or `-lat`: The latitude in degrees (North is positive. It should be a decimal value).
- `--longitude` or `-lon`: The longitude in degrees (East is positive. It should be a decimal value).
- `--render-img` or `-ri`: Pass this flag if you want to render the image from command line.
- `--render-anim` or `-ra`: Pass this flag if you want to render the animation from command line. `--render-anim` only works if `--animate` is also passed. Note: a folder called "frames" is created in the same folder as 'combined.py' to store all frames as .png files.  
  
Example command including all flags:  
```
blender --background --python combined.py -- --animate --save --time 23:59 --date 2021-08-01 --latitude 19.0760 --longitude 72.8777 --render-img --render-anim
```
Note: Short forms of the flags (mentioned above) can also be used instead of the long version in the example.