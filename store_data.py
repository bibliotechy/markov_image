import asyncio
import argparse
from databases import Database
import sqlalchemy as db
from markovimage.image import Image
import logging
import progressbar


def create_or_add_ring_to_center(center, ring):
     with engine.begin() as conn:
         if conn.execute(db.text("SELECT * from pixel2 where center = :center AND ring = :ring"), center=center, ring=ring).rowcount == 0:
             conn.execute(db.text("INSERT INTO pixel2 values(:center, :ring, :count)"), center=center, ring=ring, count=1)
         else:
             conn.execute(db.text("UPDATE pixel2 SET count = count + 1 where center = :center AND ring = :ring"), center=center, ring=ring)

async def center_and_ring_async(database, center, ring):
    row = await database.fetch_one(query="SELECT * from pixel2 where center = :center AND ring = :ring", values={"center": center, "ring": ring})
    if row:
        logging.debug(f"Row found for {center}, appending some values")
        await database.execute(query="UPDATE pixel2 SET count = count + 1 where center = :center AND ring = :ring", values={"center": center, "ring": ring})
    else:
        logging.debug(f"No row found for {center}, creating a new one")
        await database.execute(query="INSERT INTO pixel2 values(:center, :ring, :count)", values={"center": center, "ring": ring, "count": 1})


parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='image file to load into the db')
parser.add_argument('-d','--db', help='Path where leveldb will be created', default="db")
args = parser.parse_args()

logging.basicConfig(filename='out2.log', encoding='utf-8', level=logging.DEBUG)

engine = db.create_engine("postgresql://postgres:password@localhost:5433/postgres")
database = Database("postgresql://postgres:password@localhost:5433/postgres")

async def main():
    semaphore = asyncio.Semaphore(15)
    await database.connect()
    image = Image(args.file)
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=image.height()*image.width()).start()
    for i,(center, ring) in enumerate(image):
        await semaphore.acquire()
        logging.debug(f"center: {center} - rinr: {ring}")
        #create_or_add_ring_to_center(center, ring)
        await center_and_ring_async(database, center, ring)
        semaphore.release()
        bar.update(i+1)

asyncio.run(main())











