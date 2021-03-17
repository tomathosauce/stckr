from stckr import resize_static_no_stretching
from PIL import Image
import argparse, os
parser = argparse.ArgumentParser()

#https://stackoverflow.com/questions/41718892/pillow-resizing-a-gif

def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode 
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results

def get_frame_name(path, index):
    return '%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), index)

def get_naming_scheme(path,_format = "webp"):
    return '%s-resized.%s' % (''.join(os.path.basename(path).split('.')[:-1]), _format)


def extract_and_resize_frames(path, size):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(path)['mode']
    
    im = Image.open(path)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    all_frames = []
    
    try:
        while True:
            print ("frame", i)
            
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette() and p:
                im.putpalette(p)
            
            new_frame = Image.new('RGBA', im.size)
            
            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)
            
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            ff = resize_static_no_stretching(new_frame, size)

            all_frames.append(ff)

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return all_frames

def get_avg_fps(PIL_Image_object):
    #https://stackoverflow.com/questions/53364769/get-frames-per-second-of-a-gif-in-python
    
    #or use Image.open(FILENAME).info['duration']
    """ Returns the average framerate of a PIL Image object """
    PIL_Image_object.seek(0)
    frames = duration = 0
    while True:
        try:
            frames += 1
            duration += PIL_Image_object.info['duration']
            PIL_Image_object.seek(PIL_Image_object.tell() + 1)
        except EOFError:
            return frames / duration * 1000
    return None

def resize_animated(path: str, size):
    """
    Resizes the GIF to a given length:

    Args:
        path: the path to the GIF file
        save_as (optional): Path of the resized gif. If not set, the original gif will be overwritten.
        resize_to (optional): new size of the gif. Format: (int, int). If not set, the original GIF will be resized to
                              half of its size.
    """
    all_frames = extract_and_resize_frames(path, size)

    
    save_as = os.path.join(os.path.dirname(path), get_naming_scheme(path))

    print("Saving as...", save_as)

    if len(all_frames) == 1:
        print("Warning: only 1 frame found")
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)


def main():
    parser.add_argument("path")
    parser.add_argument("--size")

    args = parser.parse_args()

    path = os.path.abspath(args.path)

    if args.size:
        size = int(args.size)
    else:
        size = 512

    resize_animated(path, size)
    

if __name__ == "__main__":
    main()
