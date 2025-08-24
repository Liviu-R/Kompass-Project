import tempfile
import shutil

#Cleaning the leftover file(user_data_dir) of nodriver library to free up space
async def clean_up(driver)->None:
    
    try:
        shutil.rmtree(os.path.normpath(driver.config.user_data_dir))
    except:
        print("FILE NOT FOUND")
    