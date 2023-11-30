from tqdm import tqdm
from pathlib import Path
from animar.utils import die,debug
import requests
from tqdm import tqdm




class DownloadFile:
    def __init__(self, url, output_dir, file_name=None, session=None) -> None:
        self.url = url
        self.output_dir = output_dir
        self.file_name = file_name
        self.session = session
        self.CHUNK_SIZE = 1024 * 128  # 128 kilobyte
        self.downloaded_size = 0
        self.setup()
        
    def setup(self):
        if self.session is None:
            self.session = requests.Session()
        # Create the output directory if it doesn't exist
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        # Make the request to download the file
        self.response = self.session.get(self.url, stream=True)

        # Get the total file size from the response headers
        self.total_size = int(self.response.headers.get("content-length", 0))

        if self.file_name is None:
            disposition = self.response.headers.get("content-Disposition").split("; ")
            # find the filename
            for i in disposition:
                if "filename" in i:
                    self.file_name = i.split("=")[1].replace('"', "")
                    break
            else:
                raise Exception("No filename found")

        # Set the file path
        self.file_path = Path(self.output_dir) / self.file_name
        
        self.temp_file_path = self.file_path.with_suffix(".temp")
        self.temp_file = open(self.temp_file_path, "wb")
        
        return True
    
    def download(self):
        for chunk in self.response.iter_content(chunk_size=self.CHUNK_SIZE):
            if chunk:
                self.temp_file.write(chunk)
                self.downloaded_size += len(chunk)
            yield chunk
    def close(self):
        self.temp_file_path.rename(self.file_path)
        self.session.close()
        self.temp_file.close()
        return True
    
    
def download_file(url, output_dir, file_name=None, session=None, desc=None):
    download_file = DownloadFile(url, output_dir, file_name, session)
    # Initialize the tqdm progress bar
    progress_bar = tqdm(total=download_file.total_size, unit="B", unit_scale=True, desc=desc)
    for chunk in download_file.download():
        if chunk:
            progress_bar.update(len(chunk))
    progress_bar.close()
    download_file.close()
  
  
if __name__ == "__main__":
    link = "https://doc-10-0g-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/4t1sb3c5i86m149qtkitt679dcpsq2kp/1701110700000/03715700210059037670/*/1EzbVC-6O5XhTELRYsVrC4X5D-ivJxKDC?e=download&uuid=f5219d0b-dbbc-4442-a3a6-e0222273d87f"
    download_file(link, ".", "test.mp4")
    
