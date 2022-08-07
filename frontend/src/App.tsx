import React, {useState, useEffect} from 'react';
import './App.css';
import {Button, List, ListItem, IconButton, ListItemAvatar, Avatar, ListItemText, ListItemButton} from "@mui/material";
import DownloadIcon from '@mui/icons-material/Download';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import DeleteIcon from '@mui/icons-material/Delete';


const baseEndPt = "http://localhost:8080";
const filesEndPt = baseEndPt + "/files";

interface FetchedFile {
}

function App() {
    const [fetchedFiles, setFetchedFiles] = useState<Array<string>>();

    const uploadFile = (toUpload: File) => {
        const data = new FormData();
        data.append('file', toUpload);

        fetch(filesEndPt, {
            method: 'POST',
            body: data,
        })
            .then(() => {
                fetchFiles();
            })
            .catch(err => console.log(err))
    }

    const fetchFiles = () => {
        fetch(filesEndPt, {
            method: 'GET',
        })
            .then(res => res.json())
            .then(res => {
                setFetchedFiles(res.files ?? []);
            })
            .catch(err => console.log(err));
    }

    useEffect(() => {
        // retrieve fetched files
        fetchFiles();
    }, [])

    const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        // set file to the file object
        if (e.target.files) {
            console.log(e.target.files[0]);
            uploadFile(e.target.files[0]);
        } else {
            resetEventVal(e);
        }
    }

    const resetEventVal = (e: any) => {
        if (e.target && e.target.value) {
            e.target.value = null;
        }
    }

    const onDownload = (fileName: string) => {
        const endpt = filesEndPt + "/" + fileName;
        fetch(endpt, {
            method: 'GET',
        })
            .then(res => res.json())
            .then(res => {
                const link = document.createElement('a');
                link.href = res.url;
                link.setAttribute('download', fileName);
                link.click();
            })
            .catch(err => console.log(err));
    }

    const onDelete = (fileName: string) => {
        const endpt = filesEndPt + "/" + fileName;
        fetch(endpt, {
            method: 'DELETE',
        })
            .then(res => {fetchFiles()})
            .catch(err => console.log(err));
    }

  return (
    <div style={{
        display: 'flex',
        flexDirection: "column",
        alignItems: 'center',
        gap: "10px",
    }}>

      <div
        style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
        }}
      >

        <Button
          component={"label"}

        >
          Upload File
            <input type="file" hidden
                   onChange={(e)=> {
                onFileChange(e)
            }}
                   onClick={(e)=> {
                       resetEventVal(e);
                   }}
            />
        </Button>

      </div>

    <List>
        {
            fetchedFiles && fetchedFiles.map((fileName) => {
                return (
                    <ListItem
                        key={fileName}
                        secondaryAction={
                            <IconButton edge="end" aria-label="download" onClick={() => onDownload(fileName)}>
                                <DownloadIcon />
                            </IconButton>
                        }
                    >
                        <ListItemAvatar>
                            <Avatar>
                                <InsertDriveFileIcon />
                            </Avatar>
                        </ListItemAvatar>
                        <IconButton edge="end" aria-label="delete" onClick={() => onDelete(fileName)}>
                            <DeleteIcon />
                        </IconButton>
                        {/*<ListItemButton role={undefined} onClick={handleToggle(value)} dense>*/}
                        {/*    <IconButton edge="end" aria-label="delete" onClick={() => onDelete(fileName)}>*/}
                        {/*        <DeleteIcon />*/}
                        {/*    </IconButton>*/}
                            <ListItemText
                                primary={fileName}
                            />
                        {/*</ListItemButton>*/}
                    </ListItem>
                )
            })
        }
    </List>


    </div>
  );
}

export default App;
