"""
Chapter 4. Naive Bayesian Classification
EmailObject class
"""
import email
import sys

from bs4 import BeautifulSoup


class EmailObject(object):
  """
  Parses incoming email messages
  """
  CLRF = "\n\r\n\r"

  # TODO: Figure out what the category param is supposed to do.
  def __init__(self, infile, category=None):
    self.category = category
    if sys.version_info > (3, 0):
      # Python 3 code in this block
      self.mail = email.message_from_binary_file(infile)
    else:
      # Python 2 code in this block
      self.mail = email.message_from_file(infile)

  def subject(self):
    """
    Get message subject line
    :return: str
    """
    return self.mail.get('Subject')

  def body(self):
    """
    Get message body
    :return: str in Py3, unicode in Py2
    """
    #* Note: an email message consists of headers and payload (aka content), payload may be one of a simple text message, binary object or a structured sequence of sub-messages each with their own headers and payloads. (The latter is MIME type, such as multipart)
    payload = self.mail.get_payload()
    #! If the email is a multipart type, it converts the payload into a list and iterates over the list to separate each part into an element in parts.
    if self.mail.is_multipart():
      parts = [self._single_body(part) for part in list(payload)]
    else:
      parts = [self._single_body(self.mail)]
    decoded_parts = []
    for part in parts:
      if len(part) == 0:
        continue
      #! Handles parts which are of a byte instance by decoding them and appending to decoded_parts
      if isinstance(part, bytes):
        decoded_parts.append(part.decode('utf-8', errors='ignore'))
      else:
        decoded_parts.append(part)
    return self.CLRF.join(decoded_parts)

  @staticmethod
  def _single_body(part):
    """
    Get text from part.
    :param part: email.Message
    :return: str body or empty str if body cannot be decoded
    """
    content_type = part.get_content_type()
    try:
      body = part.get_payload(decode=True)
    except Exception:
      return ''
    #! Handles the case where the body of an email is of the html type.
    if content_type == 'text/html':
      return BeautifulSoup(body, 'html.parser').text
    elif content_type == 'text/plain':
      return body
    return ''
