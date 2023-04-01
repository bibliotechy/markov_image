import argparse
import sqlalchemy as db
import logging
from random import choices
from PIL import Image
import progressbar

from markovimage.image import Image as MarkovImage

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', default="new.jpg", help='name of the output file')
parser.add_argument('-^', '--height', default=20, help='height of the generate image', type=int)
parser.add_argument('->', '--width', default=20, help='width of the generate image', type=int)
args = parser.parse_args()

logging.basicConfig(filename='make-out.log', encoding='utf-8', level=logging.DEBUG)

database = db.create_engine("postgresql://postgres:password@localhost:5433/postgres")


class ImageMaker():
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.img = Image.new(mode="RGB", size=(args.width, args.height), color="white")
    self.markov_image = MarkovImage(pil_image=self.img)
    self.pixels = self.img.load()
    self.set_pixels = []
    self.random_hex = pick_random_hex()




def make_image():

  im = ImageMaker(args.height, args.width)
  
  try:
    im.pixels, im.set_pixels = set_coord_rgb(im.markov_image, im.pixels, [1,1], im.random_hex[0], im.set_pixels)
    for row in range(im.height):
        for column in range(im.width):
          im.pixels, im.set_pixels = set_coord_rgb(im.markov_image, im.pixels, [row,column], pick_random_hex()[0], im.set_pixels)
  except Exception:
    pass
  finally:
    im.img.show()
  # pixels[mid_h,mid_w] = rgb_from_hex(random_hex[0])

  # ring_coords = [[i,j] if ((i != None) & (j != None)) else None for i in markov_image.row_range(mid_h) for j in markov_image.column_range(mid_w) ]
  # # remove the center coord, cause we already set that.
  # ring_coords.pop(4)
  # for i, coord in enumerate(ring_coords):
  #   pixels[coord[0],coord[1]] = rgb_from_hex(random_hex[1].split(":")[i])
  
  # for coord in ring_coords:
  #   coord_ring_hexes = select_random_ring_for_hex(hex_from_rgb(pixels[coord[0],coord[1]]))
  #   coord_ring_coords = [[i,j] if ((i != None) & (j != None)) else None for i in markov_image.row_range(coord[0]) for j in markov_image.column_range(coord[1]) ]
  #   coord_ring_coords.pop(4)
  
  #   for i, _coord in enumerate(coord_ring_coords):
  #     pixels[_coord[0],_coord[1]] = rgb_from_hex(coord_ring_hexes[i])


def set_coord_rgb(mimage, pixels, coord, hex, set_pixels: list):
  """
  What this should be doing
  given a pixel coordinate it checks
    1. Has this pixel already been set, is so skip
    2. Capture values of ring pixels that have already been set
    3. Use ring pixel's values as part of sql query to find
      any matching DB entries.

      For example, if the only the pixel in the same row but previous column is set
      then we would search for rings with where the first three ring pixels match
      a hex color ([\da-e]) or empty string with a trailing colon
      followed by the known hex color with trailing colon
      followed by three more hex color or empty string with trailing colon
      folowed by a final hex color or empty sting WITHOUT a trailing colon
      SELECT * FROM pixel2 WHERE 
      ring ~ '(([\da-e]{6})?:){3}00999b:(([\da-e]{6})?:){3}(([\da-e]{6})?)' 
      ORDER BY count desc;

      If no DB record ring matches all of the known set ring pixels, then query based on 
      all but one, then all but two, etc. Which one to remove first? 
      Remove order:
      R,C
      3,3
      3,1
      1,3
      1,1
      3,2
      1,2
      2,3
      2,1



  """
  if not coord:
    return (pixels, set_pixels)
  h,w = coord
  if [h,w] not in set_pixels:
    pixels[h,w] = rgb_from_hex(hex)
  ring_coords = [[i,j] if ((i != None) & (j != None)) else None for i in mimage.row_range(h) for j in mimage.column_range(w) ]
  ring_coords.pop(4)
  ring = select_random_ring_for_hex(hex, ring_coords)
  
  for i, _coord in enumerate(ring_coords):
    if not _coord:
      continue
    _h, _w = _coord
    if [_h,_w] not in set_pixels:
      pixels[_h,_w] = rgb_from_hex(ring[i])
      set_pixels.append([_h,_w])
   
  return (pixels, set_pixels)



def pick_random_hex():
  with database.begin() as conn:
    res = conn.execute("SELECT * from pixel2 TABLESAMPLE SYSTEM (1) LIMIT 1 ;").fetchone()
    return res

def select_random_ring_for_hex(hex, ring_coords):
  with database.begin() as conn:
    res = conn.execute(db.text("SELECT * from pixel2 where center = :center and ring ~ :ring" ), center=hex, ring=ring_regex(ring_coords)).fetchall()
    if len(res) > 0:
      return choices(
        [r[1] for r in res], 
        weights=[r[2] for r in res], 
        k=1
      )[0].split(":")
    else:
      res = conn.execute(db.text("SELECT * from pixel2 where center = :center" ), center=hex).fetchall()
      if len(res) > 0:
        return choices(
          [r[1] for r in res], 
          weights=[r[2] for r in res], 
          k=1
        )[0].split(":")


def rgb_from_hex(hex):
  # import pdb
  # pdb.set_trace()
  hex = hex.lstrip('#')
  hex_length = len(hex)
  if hex_length // 3 == 0:
    import pdb
    pdb.set_trace()
  return tuple(
    int(hex[i:i + hex_length // 3], 16) 
    for i in range(0, hex_length, hex_length // 3
    )
  )

def hex_from_rgb(rgb):
  return '%02x%02x%02x' % tuple(rgb)


def ring_regex(ring_values: list):
  colon = '(([\da-e]{6})?:)'
  no_colon = '(([\da-e]{6})?)'
  regex_segments = []
  for value in ring_values[:-1] if ring_values else []:
    regex_segments.append(value if value else colon)
  regex_segments.append(ring_values[-1] if ring_values[-1] else no_colon)
  return "".join(regex_segments)




make_image()
