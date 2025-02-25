import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "./api";

export default function Dropzone() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const { getRootProps, getInputProps } = useDropzone({
    accept: "image/*",
    onDrop: (acceptedFiles) => {
      setImage(acceptedFiles[0]);
      handleUpload(acceptedFiles[0]);
    },
  });

  const handleUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("/classify", formData);
      setResult(response.data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="p-6 flex flex-col items-center">
      <div
        {...getRootProps()}
        className="border-dashed border-2 border-gray-500 p-10 rounded-lg cursor-pointer"
      >
        <input {...getInputProps()} />
        <p>Drag & drop an image here, or click to select one</p>
      </div>

      {image && <img src={URL.createObjectURL(image)} className="mt-4 w-48" alt="Uploaded" />}
      
      {result && (
        <div className="mt-4 p-4 border rounded">
          <p><strong>Classification:</strong> {result.class}</p>
          <p><strong>Test Accuracy:</strong> {result.accuracy}%</p>
        </div>
      )}
    </div>
  );
}
