from markitdown import MarkItDown

class PdfToMarkdown:
    """
    A class for converting a PDF to Markdown format using MarkItDown.
    """

    def __init__(self, pdf_path: str):
        """
        Initialize the PdfToMarkdown class.

        Parameters:
        - pdf_path (str): Path to the PDF file to convert.
        """
        self.pdf_path = pdf_path
        self.md_converter = MarkItDown()

    def convert_pdf_to_markdown(self) -> str:
        """
        Convert the PDF to Markdown format.

        Returns:
        - str: The converted Markdown text.
        """
        try:
            result = self.md_converter.convert(self.pdf_path)
            return result.text_content
        except Exception as e:
            return f"Error during conversion: {e}"
