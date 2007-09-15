"""base classes for css and stylesheets packages
"""
__all__ = []
__docformat__ = 'restructuredtext'
__author__ = '$LastChangedBy$'
__date__ = '$LastChangedDate$'
__version__ = '$LastChangedRevision$'

import xml.dom
import cssutils
from tokenize import Tokenizer
from tokenize2 import Tokenizer as Tokenizer2

class Base(object):
    """
    Base class for most CSS and StyleSheets classes

    contains helper objects
        * _log
        * _ttypes

    and functions
        * staticmethod: _normalize(x)
        * _checkReadonly()
        * _tokenize()
        * _tokensupto()
        * _valuestr()

    for inheriting classes helping parsing
    """
    _log = cssutils.log

    __tokenizer2 = Tokenizer2()
    _prods = cssutils.tokenize2.CSSProductions

    def _tokenize2(self, textortokens, aslist=False, fullsheet=False):
        """
        returns tokens of textortokens which may already be tokens in which
        case simply returns input
        """
        if isinstance(textortokens, basestring):
            if aslist:
                return [t for t in self.__tokenizer2.tokenize(
                     textortokens, fullsheet=fullsheet)]
            else:
                return self.__tokenizer2.tokenize(
                     textortokens, fullsheet=fullsheet)
        elif isinstance(textortokens, tuple):
            # a single token (like a comment)
            return [textortokens]
        else:
            return textortokens # already tokenized

    def _type(self, token):
        "type of Tokenizer2 token"
        return token[0]

    def _value(self, token):
        "value of Tokenizer2 token"
        return token[1]

    def _tokensupto2(self,
                     tokenizer,
                     token,
                     blockstartonly=False,
                     blockendonly=False,
                     propertynameendonly=False,
                     propertyvalueendonly=False,
                     propertypriorityendonly=False,
                     selectorattendonly=False,
                     funcendonly=False):
        """
        returns tokens upto end of atrule and end index
        end is defined by parameters, might be ; } ) or other

        default looks for ending "}" and ";"
        """
        ends = u';}'

        if blockstartonly: # {
            ends = u'{'
        if blockendonly: # }
            ends = u'}'
        elif propertynameendonly: # : and ; in case of an error
            ends = u':;'
        elif propertyvalueendonly: # ; or !important
            ends = (u';', u'!important')
        elif propertypriorityendonly: # ;
            ends = u';'
        elif selectorattendonly: # ]
            ends = u']'
        elif funcendonly: # )
            ends = u')'

        brace = bracket = parant = 0 # {}, [], ()
        if blockstartonly:
            brace = -1 # set to 0 with first {

        resulttokens = [token]
        for token in tokenizer:
            if self._type(token) == 'EOF':
                break

            if u'{' == self._value(token): brace += 1
            elif u'}' == self._value(token): brace -= 1
            if u'[' == self._value(token): bracket += 1
            elif u']' == self._value(token): bracket -= 1
            # function( or single (
            if u'(' == self._value(token) or \
               Base._ttypes.FUNCTION == self._type(token): parant += 1
            elif u')' == self._value(token): parant -= 1
            resulttokens.append(token)
            if self._value(token) in ends and (
                                    brace == bracket == parant == 0):
                break

        return resulttokens

    # ----

    def _S(seq, token, tokenizer=None):
        "default implementation for S token"
        pass

    def _COMMENT(seq, token, tokenizer=None):
        "default implementation for comment token"
        seq.append(cssutils.css.CSSComment([token]))

    def _EOF(seq=None, token=None, tokenizer=None):
        "default implementation for EOF token"
        return 'EOF'

    def _atrule(seq, token, tokenizer=None):
        pass#print "@rule", token

    default_productions = {
        'COMMENT': _COMMENT,
        'S': _S,
        'EOF': _EOF,
        'ATKEYWORD': _atrule
        }

    def _parse(self, seq, tokenizer, productions, default=None):
        """
        puts parsed tokens in seq by calling a production with
            (seq, tokenizer, token)

        seq
            to add rules etc to
        tokenizer
            call tokenizer.next() to get next token
        productions
            callbacks {tokentype: callback}
        default
            default callback if tokentype not in productions
        """
        prods = self.default_productions
        prods.update(productions)

        for token in tokenizer:
            typ, val, lin, col = token
            p = prods.get(typ, default)
            if p is None:
                self._log.Error('Unexpected token (%s, %s, %s, %s)' % token)
            else:
                p(seq, token, tokenizer)



    # --- OLD ---
    __tokenizer = Tokenizer()
    _ttypes = __tokenizer.ttypes

    def _tokenize(self, textortokens, _fullSheet=False):
        """
        returns tokens of textortokens which may already be tokens in which
        case simply returns input
        """
        if isinstance(textortokens, list) and\
           isinstance(textortokens[0], tuple):
            # todo: convert tokenizer 2 list to tokenizer 1 list
            return textortokens # already tokenized


        elif isinstance(textortokens, list):
            return textortokens # already tokenized
        elif isinstance(textortokens, cssutils.token.Token):
            return [textortokens] # comment is a single token
        elif isinstance(textortokens, basestring): # already string
            return self.__tokenizer.tokenize(textortokens, _fullSheet)
        else:
            if textortokens is not None:
                textortokens = unicode(textortokens)
            return self.__tokenizer.tokenize(textortokens, _fullSheet)

    @staticmethod
    def _normalize(x):
        """
        normalizes x namely replaces any \ with the empty string
        so for x=="c\olor\" return "color"

        used in Token for normalized value and CSSStyleDeclaration
        currently
        """
        return x.replace(u'\\', u'').lower()

    def _checkReadonly(self):
        "raises xml.dom.NoModificationAllowedErr if rule/... is readonly"
        if hasattr(self, '_readonly') and self._readonly:
            raise xml.dom.NoModificationAllowedErr(
                u'%s is readonly.' % self.__class__)
            return True
        return False

    def _tokensupto(self, tokens,
                    blockstartonly=False,
                    blockendonly=False,
                    propertynameendonly=False,
                    propertyvalueendonly=False,
                    propertypriorityendonly=False,
                    selectorattendonly=False,
                    funcendonly=False):
        """
        returns tokens upto end of atrule and end index
        end is defined by parameters, might be ; } ) or other

        default looks for ending "}" and ";"
        """
        ends = u';}'

        if blockstartonly: # {
            ends = u'{'
        if blockendonly: # }
            ends = u'}'
        elif propertynameendonly: # : and ; in case of an error
            ends = u':;'
        elif propertyvalueendonly: # ; or !important
            ends = (u';', u'!important')
        elif propertypriorityendonly: # ;
            ends = u';'
        elif selectorattendonly: # ]
            ends = u']'
        elif funcendonly: # )
            ends = u')'

        brace = bracket = parant = 0 # {}, [], ()
        if blockstartonly:
            brace = -1 # set to 0 with first {
        resulttokens = []
        i, imax = 0, len(tokens)
        while i < imax:
            t = tokens[i]

            if u'{' == t.value: brace += 1
            elif u'}' == t.value: brace -= 1
            if u'[' == t.value: bracket += 1
            elif u']' == t.value: bracket -= 1
            # function( or single (
            if u'(' == t.value or \
               Base._ttypes.FUNCTION == t.type: parant += 1
            elif u')' == t.value: parant -= 1

            resulttokens.append(t)

            if t.value in ends and (brace == bracket == parant == 0):
                break

            i += 1

        return resulttokens, i

    def _valuestr(self, t):
        """
        returns string value of t (t may be a string, a list of token tuples
        or a single tuple in format (type, value, line, col) or a
        tokenlist[old])
        """
        if t is None:
            return u''
        elif isinstance(t, basestring):
            return t
        elif isinstance(t, list) and isinstance(t[0], tuple):
            return u''.join([x[1] for x in t])
        elif isinstance(t, tuple): # needed?
            return self._value(t)
        else: # old
            return u''.join([x.value for x in t])

    # ----

#    def parseproduction(self, prod, expected):
#        """
#        parses a production for certain rules and returns sequence
#        if it matches expectedseq
#        """
#        prod = "NAMESPACE_SYM S* [namespace_prefix S*]? [STRING|URI] S* ';' S*"
#        for part in prod.split(' '):
#            quant = part[-1]
#            if quant != '?' and quant != '*':
#                quant = ''


