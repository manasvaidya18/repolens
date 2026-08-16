function ImportRepositoryButton({
  onImport,
  disabled,
}) {
  return (
    <button
      className="analyze-btn"
      onClick={onImport}
      disabled={disabled}
    >
      Import Repository
    </button>
  );
}

export default ImportRepositoryButton;