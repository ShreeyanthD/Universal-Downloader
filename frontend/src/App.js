import { useState } from "react";

function App() {

  const [url, setUrl] = useState("");
  const [mediaUrl, setMediaUrl] = useState("");
  const [mediaType, setMediaType] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("")

  async function handleFetch() {
    setMediaUrl("");
    setMediaType("");
    setDownloadUrl("");


     if (!url) {
    alert("Please enter URL");
    return;
    }

    
    try {
      setError("");
      setLoading(true);
    const response = await fetch(
      `${process.env.REACT_APP_API_URL}/fetch`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url })
      }
    );
    
    const data = await response.json();
    if (!response.ok) {
      setError(data.message);
      setLoading(false)
      return;
    }
    setLoading(false);

    const type = data["type"]
    setMediaType(type)

    setMediaUrl(data["preview_url"]);
    setDownloadUrl(data["download_url"]);

  } catch (error) {
    setError("Something went wrong");
    setLoading(false);
    console.log("Error:", error);

  }
}

return (
  <div
    style={{
      minHeight: "100vh",
      background: "linear-gradient(to bottom, #1a1a1a, #0f0f0f)",
      color: "white",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      fontFamily: "Arial",
      padding: "20px",
      boxSizing: "border-box",
    }}
  >
    <div
      style={{
        backgroundColor: "#1e1e1e",
        padding: "25px",
        borderRadius: "20px",
        width: "90%",
        maxWidth: "350px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "15px",
        boxShadow: "0 0 20px rgba(0,0,0,0.4)",
      }}
    >
      <h1
        style={{
          margin: 0,
          fontSize: "28px",
          textAlign: "center",
        }}
      >
        📥 Universal Downloader
      </h1>

      <p
        style={{
          marginTop: "-5px",
          color: "#aaaaaa",
          fontSize: "14px",
          textAlign: "center",
        }}
      >
        Download reels and posts instantly
      </p>

      <input
        type="text"
        placeholder="Paste Any URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "10px",
          border: "none",
          outline: "none",
          fontSize: "14px",
          boxSizing: "border-box",
        }}
      />

      <button
        onClick={handleFetch}
        style={{
          width: "100%",
          padding: "12px",
          borderRadius: "10px",
          border: "none",
          backgroundColor: "#0095f6",
          color: "white",
          fontWeight: "bold",
          cursor: "pointer",
          fontSize: "15px",
          transition: "0.2s",
        }}
      >
        {loading ? "Fetching..." : "Fetch"}
      </button>

      {error && (
        <p
          style={{
            color: "#ff4d4d",
            margin: 0,
            textAlign: "center",
          }}
        >
          {error}
        </p>
      )}

      {mediaType === "Video" && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "10px",
            width: "100%",
            backgroundColor: "#181818",
            padding: "10px",
            borderRadius: "15px",
            boxSizing: "border-box",
          }}
        >
          <video
            controls
            width="100%"
            style={{
              borderRadius: "12px",
            }}
          >
            <source src={mediaUrl} type="video/mp4" />
          </video>

          <a
            href={downloadUrl}
            download
            style={{
              width: "100%",
            }}
          >
            <button
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "10px",
                border: "none",
                backgroundColor: "#2ea44f",
                color: "white",
                fontWeight: "bold",
                cursor: "pointer",
                transition: "0.2s",
              }}
            >
              Download Video
            </button>
          </a>
        </div>
      )}

      {mediaType === "Post" && (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "10px",
            width: "100%",
            backgroundColor: "#181818",
            padding: "10px",
            borderRadius: "15px",
            boxSizing: "border-box",
          }}
        >
          <img
            src={mediaUrl}
            alt="Instagram Post"
            width="100%"
            style={{
              borderRadius: "12px",
            }}
          />

          <a
            href={downloadUrl}
            download
            style={{
              width: "100%",
            }}
          >
            <button
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "10px",
                border: "none",
                backgroundColor: "#2ea44f",
                color: "white",
                fontWeight: "bold",
                cursor: "pointer",
                transition: "0.2s",
              }}
            >
              Download Post
            </button>
          </a>
        </div>
      )}

      <p
        style={{
          fontSize: "12px",
          color: "#777",
          marginTop: "5px",
          textAlign: "center",
        }}
      >
        Built with React + Flask
      </p>
    </div>
  </div>
);
}

export default App;