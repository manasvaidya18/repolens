function RepoInput({ url, setUrl }) {
  return (
    <input
      className="repo-input"
      type="text"
      placeholder="Enter GitHub repository URL"
      value={url}
      onChange={(event) =>
        setUrl(event.target.value)
      }
    />
  );
}

export default RepoInput;