from PIL import Image
import os, argparse, time, glob, zipfile
from shutil import copyfile
parser = argparse.ArgumentParser()

def resize_static_no_stretching(image, size=512):
    image = image.convert('RGBA')
    width, height = image.size

    if height > width:
        factor = size / height
    else:
        factor = size / width

    new_size = (int(round(width * factor)), int(round(height * factor)))

    image = image.resize(new_size, resample=Image.ANTIALIAS)

    print("\nResizing to {}".format(new_size))

    new_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    y = (size - image.size[1]) // 2
    x = (size - image.size[0]) // 2
    new_image.paste(image, (x, y))
    return new_image

STICKER_DIMENSIONS = (512,512)

def create_pack(title: str, 
                author: str, 
                sticker_thumbnail: str, 
                path: str, 
                ignore_webp = False, 
                only_webp = False, 
                no_stretching = True, 
                gif = False):
    stamp = time.time()
    var = 500
    count = 1000
    compressed = []

    if ignore_webp and only_webp:
        print("Both --ignore_webp and --only_webp cannot be true!")
        exit()

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    sub_path = os.path.join(path, title)

    print(ignore_webp)
    print("Path: {}".format(path))

    try: 
        os.mkdir(sub_path)
    except OSError as error: 
        print(error)   

    if os.path.isdir(sub_path):
        to_be_deleted = glob.glob(sub_path)
        try:
            for fdeleted in to_be_deleted:
                os.remove(fdeleted)
        except PermissionError as PermError:
            print(PermError)

    zip = zipfile.ZipFile(os.path.join(sub_path, title + ".wastickers"), 'w')

    t_name = str(int(stamp)+count) + ".png"
    thumbnail_path = os.path.join(sub_path, t_name)
    f_img = os.path.join(path, sticker_thumbnail)
    img = Image.open(f_img)
    img = img.resize((96,96))
    img.save(thumbnail_path , "png")
    print(sticker_thumbnail, thumbnail_path)

    compressed.append(thumbnail_path)

    zip.write(thumbnail_path, arcname="\\"+t_name, compress_type = zipfile.ZIP_DEFLATED)

    for file in files:
        file_lowered = file.lower()
        if file_lowered.endswith(('.png', '.jpg', '.jpeg', ".webp", ".gif")):

            if file_lowered.endswith((".gif")) and gif == True:
                continue

            count = count + var
            name = str(int(stamp)+count) + ".webp"
            s_path = os.path.join(sub_path, name )
            f_img = os.path.join(path,file)
            img = Image.open(f_img)
            
            save_file = True

            if file_lowered.endswith((".gif")):
                img.save(s_path ,"webp",  duration=img.info["duration"], save_all=True)
            elif file_lowered.endswith((".webp")) and not ignore_webp:
                copyfile(f_img, s_path)
            else:
                if not only_webp:
                    if no_stretching:
                        img = resize_static_no_stretching(img)
                    else:
                        img = img.resize(STICKER_DIMENSIONS)
                    img.save(s_path , "webp")
                else:
                    save_file = False

            if save_file:
                print("Saving {} to {}".format( file, s_path))

                compressed.append(s_path)

                zip.write(s_path, arcname="\\"+name, compress_type = zipfile.ZIP_DEFLATED)
                
            
    atp = os.path.join(sub_path, "author.txt")
    at = open(atp, "w")
    at.write(author)
    at.close()

    tit = os.path.join(sub_path, "title.txt")
    ti = open(tit, "w")
    ti.write(title)
    ti.close()

    zip.write(atp , "author.txt", compress_type = zipfile.ZIP_DEFLATED)
    zip.write(tit , "title.txt", compress_type = zipfile.ZIP_DEFLATED)

if __name__ == "__main__":
    parser.add_argument("title")
    parser.add_argument("author")
    parser.add_argument("sticker_thumbnail")
    parser.add_argument("--path")
    parser.add_argument("--ignore_webp", action="store_true")
    parser.add_argument("--only_webp", action="store_true")
    parser.add_argument("--no_stretching", action="store_true")
    parser.add_argument("--gif", action="store_true")
    args = parser.parse_args()

    if not args.path:
        path = os.path.dirname(os.path.realpath(__file__))
    else:
        path = os.path.abspath(args.path)

    create_pack(args.title, 
                args.author, 
                args.sticker_thumbnail, 
                path, 
                args.ignore_webp, 
                args.only_webp, 
                args.no_stretching, 
                args.gif)