import { useState, useEffect, useRef } from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { CssBaseline, GlobalStyles, Alert } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#deb887", // Light brown color
    },
    secondary: {
      main: "#f5deb3", // Wheat color
    },
    background: {
      default: "#f5f5dc", // Beige background color
    },
  },
  typography: {
    h6: {
      color: "#8b4513", // Darker color for labels
    },
  },
});

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const formRef = useRef(null);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null);
      }, 5000); // Clear error after 5 seconds

      return () => clearTimeout(timer);
    }
  }, [error]);

  useEffect(() => {
    if (success) {
      const successTimer = setTimeout(() => {
        setSuccess(null);
      }, 5000); // Clear success message after 5 seconds

      return () => clearTimeout(successTimer);
    }
  }, [success]);

  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null); // Clear any previous errors
    setSuccess(null); // Clear any previous success messages

    const url = process.env.REACT_APP_API_GATEWAY_URL;
    const file = event.target.file.files[0];
    const email = event.target.email.value;

    if (url === null || url === undefined) {
      setError("The API has not been set up correctly.");
      setLoading(false);
      return;
    }

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        fileName: file.name,
        email: email,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.preSignedURL) {
          fetch(data.preSignedURL, {
            method: "PUT",
            headers: {
              "Content-Type": file.type,
              "x-amz-tagging": `email=${email}`,
            },
            body: file,
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error("Failed to upload the file to the input bucket.");
              }
              console.log(response);
              setSuccess("The audio book is being generated. You will receive an email once it is ready.");
            })
            .catch((e) => {
              setError("There was an issue while uploading the file to the input bucket.");
              console.log(e);
            });
        } else {
          setError(data.message || "An error occurred.");
          console.log(data.message);
        }
      })
      .catch((e) => {
        setError("The request failed due to a server issue.");
        console.log(e);
      })
      .finally(() => {
        setLoading(false);
        formRef.current.reset();
      });
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <GlobalStyles styles={{ body: { backgroundColor: "#e0ffe0" } }} />
      <Container
        maxWidth="sm"
        sx={{ mt: 5, p: 4, bgcolor: "background.default", borderRadius: 1, boxShadow: 3 }}
      >
        <Typography
          variant="h4"
          component="h1"
          gutterBottom
          align="center"
          sx={{ color: "#8b4513" }}
        >
          Create an Audiobook!
        </Typography>
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" sx={{ mb: 3 }}>
            {success}
          </Alert>
        )}
        <form ref={formRef} onSubmit={(e) => handleSubmit(e)}>
          <Box mb={3}>
            <Typography variant="h6">Upload file</Typography>
            <TextField
              id="file"
              name="file"
              type="file"
              slotProps={{ htmlInput: { accept: ".txt" }, inputLabel: { shrink: true } }}
              fullWidth
              required
            />
          </Box>

          <Box mb={3}>
            <Typography variant="h6">Email address</Typography>
            <TextField
              type="email"
              id="email"
              name="email"
              placeholder="ex@email.com"
              fullWidth
              required
            />
          </Box>

          <Box display="flex" justifyContent="space-between">
            <Button type="reset" variant="contained" color="secondary">
              Reset
            </Button>
            <Button type="submit" variant="contained" color="primary" disabled={loading}>
              Generate The Audio book
            </Button>
          </Box>
        </form>
      </Container>
    </ThemeProvider>
  );
}

export default App;