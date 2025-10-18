from pathlib import Path

import pandas as pd
import pytest
from Conversation import ChatGPTConversation  # adjust import to your file

# Path to your sample JSON file
SAMPLE_JSON = Path("./assets/conversations.json")


@pytest.fixture
def conv():
    """Return a ChatGPTConversationDF instance for testing."""
    return ChatGPTConversation(SAMPLE_JSON)


def testLoadData(conv):
    """Test that the DataFrame loads correctly."""
    df = conv.get_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert all(
        col in df.columns
        for col in ["conv_index", "conversation_title", "node_id", "role", "text"]
    )


def testGetConversations(conv):
    """Test getting conversation summaries."""
    summary = conv.get_conversations()
    assert isinstance(summary, pd.DataFrame)
    assert "conversation_title" in summary.columns
    assert "message_count" in summary.columns
    # message_count should be >= 0
    assert (summary["message_count"] >= 0).all()


def testGetMessagesByConv(conv):
    """Test retrieving messages for a specific conversation."""
    df_all = conv.get_dataframe()
    first_index = df_all["conv_index"].iloc[0]
    df_conv = conv.get_messages_by_conv(first_index)
    assert isinstance(df_conv, pd.DataFrame)
    assert len(df_conv) > 0
    assert (df_conv["conv_index"] == first_index).all()


def testSearchMessages(conv):
    """Test searching for messages containing a query string."""
    df_search = conv.search_messages("INFP")
    assert isinstance(df_search, pd.DataFrame)
    for text in df_search["text"]:
        assert "INFP".lower() in text.lower()

    # Also test search within a specific conversation
    first_index = conv.get_dataframe()["conv_index"].iloc[0]
    df_search_conv = conv.search_messages("INFP", conv_index=first_index)
    assert (df_search_conv["conv_index"] == first_index).all()


def testMessageTextIsString(conv):
    """Ensure all 'text' values are strings."""
    df = conv.get_dataframe()
    assert df["text"].map(lambda x: isinstance(x, str)).all()
