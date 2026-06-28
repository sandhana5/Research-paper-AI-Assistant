from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text):
    """
    Splits a large document into smaller overlapping chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = splitter.split_text(text)

    return chunks