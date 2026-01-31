"""
Regex to ε-NFA Dönüşümü
Thompson Construction Algoritması
"""
from typing import Set, Dict, List, Tuple, Optional, Generator
from .nfa import NFA


class RegexToNFA:
    """
    Thompson Construction algoritması ile Regex -> ε-NFA dönüşümü
    
    Desteklenen operatörler:
        - Concatenation (ab)
        - Union (a|b)
        - Kleene Star (a*)
        - Kleene Plus (a+)
        - Optional (a?)
        - Grouping ((ab))
        - Escape (\\* for literal *)
    """
    
    EPSILON = 'ε'
    OPERATORS = {'|', '*', '+', '?', '(', ')'}
    
    def __init__(self):
        self.state_counter = 0
        self.steps: List[dict] = []
    
    def _new_state(self) -> str:
        """Yeni durum oluştur"""
        state = f"s{self.state_counter}"
        self.state_counter += 1
        return state
    
    def _create_basic_nfa(self, symbol: str) -> Tuple[str, str, Dict, Set]:
        """
        Tek sembol için temel NFA oluştur
        
        Returns:
            (start, accept, transitions, states)
        """
        start = self._new_state()
        accept = self._new_state()
        
        transitions = {
            start: {symbol: {accept}},
            accept: {}
        }
        states = {start, accept}
        
        return start, accept, transitions, states
    
    def _create_epsilon_nfa(self) -> Tuple[str, str, Dict, Set]:
        """Sadece epsilon geçişi olan NFA"""
        start = self._new_state()
        accept = self._new_state()
        
        transitions = {
            start: {self.EPSILON: {accept}},
            accept: {}
        }
        states = {start, accept}
        
        return start, accept, transitions, states
    
    def _concatenate(
        self, 
        nfa1: Tuple[str, str, Dict, Set],
        nfa2: Tuple[str, str, Dict, Set]
    ) -> Tuple[str, str, Dict, Set]:
        """
        İki NFA'yı birleştir (concatenation)
        
        nfa1 -> nfa2
        """
        start1, accept1, trans1, states1 = nfa1
        start2, accept2, trans2, states2 = nfa2
        
        # Accept1'den start2'ye epsilon geçişi
        transitions = {}
        
        # NFA1'in geçişlerini kopyala
        for state, trans in trans1.items():
            transitions[state] = {s: set(t) for s, t in trans.items()}
        
        # NFA2'nin geçişlerini kopyala
        for state, trans in trans2.items():
            transitions[state] = {s: set(t) for s, t in trans.items()}
        
        # Accept1'den start2'ye epsilon bağlantısı
        if accept1 not in transitions:
            transitions[accept1] = {}
        if self.EPSILON not in transitions[accept1]:
            transitions[accept1][self.EPSILON] = set()
        transitions[accept1][self.EPSILON].add(start2)
        
        states = states1 | states2
        
        return start1, accept2, transitions, states
    
    def _union(
        self,
        nfa1: Tuple[str, str, Dict, Set],
        nfa2: Tuple[str, str, Dict, Set]
    ) -> Tuple[str, str, Dict, Set]:
        """
        İki NFA'yı union ile birleştir (a|b)
        """
        start1, accept1, trans1, states1 = nfa1
        start2, accept2, trans2, states2 = nfa2
        
        new_start = self._new_state()
        new_accept = self._new_state()
        
        transitions = {}
        
        # Her iki NFA'nın geçişlerini kopyala
        for state, trans in trans1.items():
            transitions[state] = {s: set(t) for s, t in trans.items()}
        for state, trans in trans2.items():
            transitions[state] = {s: set(t) for s, t in trans.items()}
        
        # Yeni başlangıçtan her iki NFA'ya epsilon
        transitions[new_start] = {self.EPSILON: {start1, start2}}
        
        # Her iki accept'ten yeni accept'e epsilon
        if accept1 not in transitions:
            transitions[accept1] = {}
        if self.EPSILON not in transitions[accept1]:
            transitions[accept1][self.EPSILON] = set()
        transitions[accept1][self.EPSILON].add(new_accept)
        
        if accept2 not in transitions:
            transitions[accept2] = {}
        if self.EPSILON not in transitions[accept2]:
            transitions[accept2][self.EPSILON] = set()
        transitions[accept2][self.EPSILON].add(new_accept)
        
        transitions[new_accept] = {}
        
        states = states1 | states2 | {new_start, new_accept}
        
        return new_start, new_accept, transitions, states
    
    def _kleene_star(
        self,
        nfa: Tuple[str, str, Dict, Set]
    ) -> Tuple[str, str, Dict, Set]:
        """
        Kleene star (a*)
        """
        start, accept, trans, states = nfa
        
        new_start = self._new_state()
        new_accept = self._new_state()
        
        transitions = {}
        
        # Orijinal geçişleri kopyala
        for state, t in trans.items():
            transitions[state] = {s: set(targets) for s, targets in t.items()}
        
        # Yeni başlangıçtan orijinal başlangıça ve yeni accept'e epsilon
        transitions[new_start] = {self.EPSILON: {start, new_accept}}
        
        # Orijinal accept'ten orijinal başlangıça ve yeni accept'e epsilon
        if accept not in transitions:
            transitions[accept] = {}
        if self.EPSILON not in transitions[accept]:
            transitions[accept][self.EPSILON] = set()
        transitions[accept][self.EPSILON].add(start)
        transitions[accept][self.EPSILON].add(new_accept)
        
        transitions[new_accept] = {}
        
        states = states | {new_start, new_accept}
        
        return new_start, new_accept, transitions, states
    
    def _kleene_plus(
        self,
        nfa: Tuple[str, str, Dict, Set]
    ) -> Tuple[str, str, Dict, Set]:
        """
        Kleene plus (a+) = aa*
        """
        start, accept, trans, states = nfa
        
        new_start = self._new_state()
        new_accept = self._new_state()
        
        transitions = {}
        
        for state, t in trans.items():
            transitions[state] = {s: set(targets) for s, targets in t.items()}
        
        # Yeni başlangıçtan orijinal başlangıça epsilon
        transitions[new_start] = {self.EPSILON: {start}}
        
        # Orijinal accept'ten orijinal başlangıça ve yeni accept'e epsilon
        if accept not in transitions:
            transitions[accept] = {}
        if self.EPSILON not in transitions[accept]:
            transitions[accept][self.EPSILON] = set()
        transitions[accept][self.EPSILON].add(start)
        transitions[accept][self.EPSILON].add(new_accept)
        
        transitions[new_accept] = {}
        
        states = states | {new_start, new_accept}
        
        return new_start, new_accept, transitions, states
    
    def _optional(
        self,
        nfa: Tuple[str, str, Dict, Set]
    ) -> Tuple[str, str, Dict, Set]:
        """
        Optional (a?)
        """
        start, accept, trans, states = nfa
        
        new_start = self._new_state()
        new_accept = self._new_state()
        
        transitions = {}
        
        for state, t in trans.items():
            transitions[state] = {s: set(targets) for s, targets in t.items()}
        
        # Yeni başlangıçtan orijinal başlangıça ve yeni accept'e epsilon
        transitions[new_start] = {self.EPSILON: {start, new_accept}}
        
        # Orijinal accept'ten yeni accept'e epsilon
        if accept not in transitions:
            transitions[accept] = {}
        if self.EPSILON not in transitions[accept]:
            transitions[accept][self.EPSILON] = set()
        transitions[accept][self.EPSILON].add(new_accept)
        
        transitions[new_accept] = {}
        
        states = states | {new_start, new_accept}
        
        return new_start, new_accept, transitions, states
    
    def _tokenize(self, regex: str) -> List[str]:
        """
        Regex'i token'lara ayır
        Concatenation için özel '·' karakteri ekle
        """
        tokens = []
        i = 0
        
        while i < len(regex):
            char = regex[i]
            
            # Escape karakteri
            if char == '\\' and i + 1 < len(regex):
                tokens.append(regex[i + 1])
                i += 2
                continue
            
            tokens.append(char)
            i += 1
        
        # Concatenation operatörü ekle
        result = []
        for i, token in enumerate(tokens):
            result.append(token)
            
            if i + 1 < len(tokens):
                current = token
                next_token = tokens[i + 1]
                
                # Concatenation gerekli mi?
                if (current not in {'|', '('} and 
                    next_token not in {'|', '*', '+', '?', ')'}):
                    result.append('·')  # Concatenation operatörü
        
        return result
    
    def _to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Infix'ten postfix'e dönüştür (Shunting-yard algoritması)
        """
        precedence = {'|': 1, '·': 2, '*': 3, '+': 3, '?': 3}
        output = []
        operator_stack = []
        
        for token in tokens:
            if token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack:
                    operator_stack.pop()  # '(' kaldır
            elif token in precedence:
                while (operator_stack and 
                       operator_stack[-1] != '(' and
                       operator_stack[-1] in precedence and
                       precedence[operator_stack[-1]] >= precedence[token]):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                # Operand (sembol)
                output.append(token)
        
        while operator_stack:
            output.append(operator_stack.pop())
        
        return output
    
    def convert(self, regex: str) -> NFA:
        """
        Regex'i ε-NFA'ya dönüştür
        
        Args:
            regex: Regular expression
            
        Returns:
            ε-NFA
        """
        for _ in self.convert_full(regex):
            pass
        
        return self._final_nfa
    
    def convert_full(self, regex: str) -> Generator[dict, None, NFA]:
        """
        Adım adım regex -> ε-NFA dönüşümü
        
        Yields:
            Her adımın bilgisi
            
        Returns:
            Oluşturulan NFA
        """
        self.state_counter = 0
        self.steps = []
        
        if not regex:
            # Boş regex için epsilon NFA
            start, accept, transitions, states = self._create_epsilon_nfa()
            self._final_nfa = NFA(states, set(), transitions, start, {accept})
            yield {
                'type': 'final',
                'step': 0,
                'description': 'Boş regex için ε-NFA oluşturuldu',
                'nfa': self._final_nfa
            }
            return self._final_nfa
        
        # Tokenize ve postfix'e çevir
        tokens = self._tokenize(regex)
        postfix = self._to_postfix(tokens)
        
        yield {
            'type': 'init',
            'step': 0,
            'description': f"Regex: {regex}\nTokens: {tokens}\nPostfix: {postfix}",
            'regex': regex,
            'tokens': tokens,
            'postfix': postfix
        }
        
        # Postfix evaluation
        stack = []
        step_num = 1
        
        for token in postfix:
            if token == '·':
                # Concatenation
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                result = self._concatenate(nfa1, nfa2)
                stack.append(result)
                
                step_info = {
                    'type': 'concatenation',
                    'step': step_num,
                    'description': f"Concatenation: NFA1 · NFA2",
                    'nfa_states': result[3],
                    'nfa_start': result[0],
                    'nfa_accept': result[1],
                    'nfa_transitions': result[2]
                }
                self.steps.append(step_info)
                yield step_info
                
            elif token == '|':
                # Union
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                result = self._union(nfa1, nfa2)
                stack.append(result)
                
                step_info = {
                    'type': 'union',
                    'step': step_num,
                    'description': f"Union: NFA1 | NFA2",
                    'nfa_states': result[3],
                    'nfa_start': result[0],
                    'nfa_accept': result[1],
                    'nfa_transitions': result[2]
                }
                self.steps.append(step_info)
                yield step_info
                
            elif token == '*':
                # Kleene star
                nfa = stack.pop()
                result = self._kleene_star(nfa)
                stack.append(result)
                
                step_info = {
                    'type': 'kleene_star',
                    'step': step_num,
                    'description': f"Kleene Star: NFA*",
                    'nfa_states': result[3],
                    'nfa_start': result[0],
                    'nfa_accept': result[1],
                    'nfa_transitions': result[2]
                }
                self.steps.append(step_info)
                yield step_info
                
            elif token == '+':
                # Kleene plus
                nfa = stack.pop()
                result = self._kleene_plus(nfa)
                stack.append(result)
                
                step_info = {
                    'type': 'kleene_plus',
                    'step': step_num,
                    'description': f"Kleene Plus: NFA+",
                    'nfa_states': result[3],
                    'nfa_start': result[0],
                    'nfa_accept': result[1],
                    'nfa_transitions': result[2]
                }
                self.steps.append(step_info)
                yield step_info
                
            elif token == '?':
                # Optional
                nfa = stack.pop()
                result = self._optional(nfa)
                stack.append(result)
                
                step_info = {
                    'type': 'optional',
                    'step': step_num,
                    'description': f"Optional: NFA?",
                    'nfa_states': result[3],
                    'nfa_start': result[0],
                    'nfa_accept': result[1],
                    'nfa_transitions': result[2]
                }
                self.steps.append(step_info)
                yield step_info
                
            else:
                # Sembol
                result = self._create_basic_nfa(token)
                stack.append(result)
                
                step_info = {
                    'type': 'basic',
                    'step': step_num,
                    'description': f"Temel NFA: '{token}'",
                    'symbol': token,
                    'nfa_states': result[3],
                    'nfa_start': result[0],
                    'nfa_accept': result[1],
                    'nfa_transitions': result[2]
                }
                self.steps.append(step_info)
                yield step_info
            
            step_num += 1
        
        # Final NFA
        if stack:
            start, accept, transitions, states = stack[0]
            
            # Alfabeyi bul
            alphabet = set()
            for trans in transitions.values():
                for symbol in trans.keys():
                    if symbol != self.EPSILON:
                        alphabet.add(symbol)
            
            self._final_nfa = NFA(states, alphabet, transitions, start, {accept})
            
            final_info = {
                'type': 'final',
                'step': step_num,
                'description': f"Final ε-NFA oluşturuldu!\n"
                              f"Durumlar: {len(states)}\n"
                              f"Alfabe: {alphabet}",
                'nfa': self._final_nfa
            }
            self.steps.append(final_info)
            yield final_info
            
            return self._final_nfa
        
        raise ValueError("Geçersiz regex")
    
    def get_all_steps(self) -> List[dict]:
        """Tüm adımları döndür"""
        return self.steps


def regex_to_nfa(regex: str) -> Tuple[NFA, List[dict]]:
    """
    Convenience function: Regex'i ε-NFA'ya dönüştür
    
    Args:
        regex: Regular expression
        
    Returns:
        (ε-NFA, adımlar listesi)
    """
    converter = RegexToNFA()
    nfa = converter.convert(regex)
    return nfa, converter.get_all_steps()
