# -*- coding: utf-8 -*-
"""Parser for PL/SQL Developer Recall files."""

import os

import construct

class UnableToParseFile(Exception):
    pass

class PlsRecallObject(object):
    """Convenience class for a PL/SQL Recall file container."""

    DATA_TYPE = u'PLSRecall:event'

    def __init__(self, sequence, time, user, database, query):
        """Initializes the event object.
        Args:
          sequence: Sequence indicates the order of execution.
          time: the Delphi time value when the entry was created.
          username: The username that made the query.
          database_name: String containing the database name.
          query: String containing the PL/SQL query.
        """
        self.time = time
        self.database_name = database
        self.query = query
        self.sequence = sequence
        self.username = user


class PlsRecallParser(object):
    """Parse PL/SQL Recall files.
    Parser is based on a::
      TRecallRecord = packed record
        Sequence: Integer;
        TimeStamp: TDateTime;
        Username: array[0..30] of Char;
        Database: array[0..80] of Char;
        Text: array[0..4000] of Char;
      end;
      Delphi TDateTime is a little endian 64-bit
      floating point without any time zone information
    """

    _INITIAL_FILE_OFFSET = None
    _PLS_KEYWORD = frozenset([
        u'begin', u'commit', u'create', u'declare', u'drop', u'end', u'exception',
        u'execute', u'insert', u'replace', u'rollback', u'select', u'set',
        u'update'])

    # 6 * 365 * 24 * 60 * 60 * 1000000.
    _SIX_YEARS_IN_MICRO_SECONDS = 189216000000000

    NAME = u'pls_recall'
    DESCRIPTION = u'Parser for PL/SQL Recall files.'

    PLS_STRUCT = construct.Struct(
        u'PL/SQL_Recall',
        construct.ULInt32(u'Sequence'),
        construct.LFloat64(u'TimeStamp'),
        construct.String(u'Username', 31, None, b'\x00'),
        construct.String(u'Database', 81, None, b'\x00'),
        construct.String(u'Query', 4001, None, b'\x00'))

    def ParseFileObject(self, file_object, **kwargs):
        """Parses a PLSRecall.dat file-like object.
        Args:
          parser_mediator: A parser mediator object (instance of ParserMediator).
          file_object: A file-like object.
        Raises:
          UnableToParseFile: when the file cannot be parsed.
        """
        _objectList = list()
        try:
            is_pls = self.VerifyFile(file_object)
        except (IOError, construct.FieldError) as exception:
            raise UnableToParseFile((
                u'Not a PLSrecall File, unable to parse.'
                u'with error: {0:s}').format(exception))

        if not is_pls:
            raise UnableToParseFile(
                u'Not a PLSRecall File, unable to parse.')

        file_object.seek(0, os.SEEK_SET)
        pls_record = self.PLS_STRUCT.parse_stream(file_object)

        while pls_record:
            _object = PlsRecallObject(
                pls_record.TimeStamp, pls_record.Sequence, pls_record.Username,
                pls_record.Database, pls_record.Query)

            _objectList.append(_object)
            try:
                pls_record = self.PLS_STRUCT.parse_stream(file_object)
            except construct.FieldError:
                # The code has reached the end of file (EOF).
                break

        return _objectList

    def VerifyFile(self, file_object):

        return True

