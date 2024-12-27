import { useState, useRef } from "react";
import axios from "axios";
import styled from "styled-components";
import toast, { Toaster } from "react-hot-toast";

// Define styled components for styling
const WebcamContainer = styled.div`
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
`;

const WebcamVideo = styled.video`
  width: 100%;
  border-radius: 10px;
`;

const PreviewImg = styled.img`
  width: 100%;
  border-radius: 10px;
`;

const WebcamCanvas = styled.canvas`
  display: none; /* Hide canvas by default */
`;

const WebcamButton = styled.button`
  background-color: #fff;
  color: #333;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const ActorList = styled.div`
  margin-top: 20px;
  text-align: center;
`;

const ActorCard = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;
`;

const ActorImage = styled.img`
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
`;

const WebcamCapture = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [mediaStream, setMediaStream] = useState<MediaStream | null>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [actors, setActors] = useState<any[]>([]);

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setMediaStream(stream);
    } catch (error) {
      console.error("Error accessing webcam", error);
    }
  };

  const stopWebcam = () => {
    if (mediaStream) {
      mediaStream.getTracks().forEach((track) => {
        track.stop();
      });
      setMediaStream(null);
    }
  };

  const captureImage = async () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext("2d");

      // Set canvas dimensions to match video stream
      if (context && video.videoWidth && video.videoHeight) {
        canvas.width = video.videoWidth / 2;
        canvas.height = video.videoHeight / 2;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Get image data URL from canvas
        const imageDataUrl = canvas.toDataURL("image/jpeg");

        const promise = new Promise(async (resolve, reject) => {
          canvas.toBlob(async (blob) => {
            if (!blob) {
              reject(new Error("Blob creation failed"));
              return;
            }

            const formData = new FormData();
            formData.append("file", blob, "image.jpg");

            try {
              const response = await axios.post(
                import.meta.env.VITE_BACKEND_URL + "api/get_celeb",
                formData,
                {
                  headers: {
                    "Content-Type": "multipart/form-data",
                  },
                }
              );
              // Set received actor data
              setActors(response.data.actors || []);
              resolve(response);
            } catch (error) {
              reject(error);
            }
          }, "image/jpeg");
        });

        toast.promise(promise, {
          loading: "Processing image...",
          success: "Image processed successfully!",
          error: "Error occurred while processing the image.",
        },
        {duration: 3000}
      );

        // Set the captured image
        setCapturedImage(imageDataUrl);

        // Stop the webcam
        stopWebcam();
      }
    }
  };

  const resetState = () => {
    stopWebcam();
    setCapturedImage(null);
    setActors([]); // Clear actor data
  };

  return (
    <WebcamContainer>
      <Toaster />
      {capturedImage ? (
        <>
          <PreviewImg src={capturedImage} className="captured-image" />
          <WebcamButton onClick={resetState}>Reset</WebcamButton>
          <ActorList>
            {actors.map((actor, index) => (
              <ActorCard key={index}>
                <ActorImage
                  src={"data:image/jpeg;base64," + actor.image}
                  alt={actor.name}
                />
                <div>
                  <p>
                    <strong>{actor.name}</strong>
                  </p>
                  <p>Score: {actor.score.toFixed(2)}</p>
                </div>
              </ActorCard>
            ))}
          </ActorList>
        </>
      ) : (
        <>
          <WebcamVideo ref={videoRef} autoPlay muted />
          <WebcamCanvas ref={canvasRef} />
          {!videoRef.current ? (
            <WebcamButton onClick={startWebcam}>Start</WebcamButton>
          ) : (
            <WebcamButton onClick={captureImage}>Capture</WebcamButton>
          )}
        </>
      )}
    </WebcamContainer>
  );
};

export default WebcamCapture;
