"""
DFA Minimization Algoritması
Table-Filling (Myhill-Nerode) yöntemi ile DFA minimizasyonu
"""
from typing import Set, Dict, List, Tuple, Optional, Generator
from .dfa import DFA


class DFAMinimization:
    """
    DFA Minimization sınıfı
    Table-Filling algoritması kullanır
    """
    
    def __init__(self, dfa: DFA):
        """
        Args:
            dfa: Minimize edilecek DFA
        """
        self.original_dfa = dfa
        self.dfa = dfa.remove_unreachable_states().make_complete()
        self.states = sorted(self.dfa.states)
        self.n = len(self.states)
        self.state_index = {s: i for i, s in enumerate(self.states)}
        
        # Ayırt edilebilirlik tablosu (distinguishable pairs)
        # table[i][j] = True eğer states[i] ve states[j] ayırt edilebilir
        self.table: List[List[Optional[bool]]] = [
            [None for _ in range(self.n)] for _ in range(self.n)
        ]
        
        self.steps: List[dict] = []
        self.partition: List[Set[str]] = []
    
    def _mark_distinguishable(self, i: int, j: int, reason: str = "") -> bool:
        """İki durumu ayırt edilebilir olarak işaretle"""
        if i > j:
            i, j = j, i
        
        if self.table[i][j] is None:
            self.table[i][j] = True
            return True
        return False
    
    def _is_distinguishable(self, i: int, j: int) -> Optional[bool]:
        """İki durumun ayırt edilebilir olup olmadığını kontrol et"""
        if i > j:
            i, j = j, i
        return self.table[i][j]
    
    def _get_partition(self) -> List[Set[str]]:
        """Mevcut tablodan partition oluştur"""
        # Union-Find benzeri yaklaşım
        parent = list(range(self.n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py
        
        # Ayırt edilemeyen durumları birleştir
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if not self._is_distinguishable(i, j):
                    union(i, j)
        
        # Grupları oluştur
        groups: Dict[int, Set[str]] = {}
        for i in range(self.n):
            root = find(i)
            if root not in groups:
                groups[root] = set()
            groups[root].add(self.states[i])
        
        return list(groups.values())
    
    def minimize_full(self) -> Generator[dict, None, DFA]:
        """
        Adım adım minimizasyon
        
        Yields:
            Her adımın bilgisi
            
        Returns:
            Minimize edilmiş DFA
        """
        # Adım 0: Başlangıç
        step_info = {
            'type': 'init',
            'step': 0,
            'description': f"DFA hazırlanıyor...\n"
                          f"Durumlar: {{{', '.join(self.states)}}}\n"
                          f"Kabul durumları: {{{', '.join(sorted(self.dfa.accept_states))}}}",
            'partition': self._get_partition(),
            'table': [row[:] for row in self.table]
        }
        self.steps.append(step_info)
        yield step_info
        
        # Adım 1: Kabul ve red durumlarını ayır
        non_accept = self.dfa.states - self.dfa.accept_states
        
        marked_pairs = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                si, sj = self.states[i], self.states[j]
                # Biri kabul, diğeri değilse ayırt edilebilir
                if (si in self.dfa.accept_states) != (sj in self.dfa.accept_states):
                    if self._mark_distinguishable(i, j, "accept/non-accept"):
                        marked_pairs.append((si, sj))
        
        step_info = {
            'type': 'base_case',
            'step': 1,
            'description': f"Temel durum: Kabul ve red durumları ayırt edilir.\n"
                          f"İşaretlenen çiftler: {marked_pairs}",
            'marked_pairs': marked_pairs,
            'partition': self._get_partition(),
            'table': [row[:] for row in self.table]
        }
        self.steps.append(step_info)
        yield step_info
        
        # Adım 2+: İteratif olarak ayırt edilebilir çiftleri bul
        iteration = 2
        changed = True
        
        while changed:
            changed = False
            marked_this_round = []
            
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    # Zaten işaretlenmişse atla
                    if self._is_distinguishable(i, j):
                        continue
                    
                    si, sj = self.states[i], self.states[j]
                    
                    # Her sembol için kontrol et
                    for symbol in self.dfa.alphabet:
                        ti = self.dfa.transition(si, symbol)
                        tj = self.dfa.transition(sj, symbol)
                        
                        if ti is None or tj is None:
                            continue
                        
                        if ti == tj:
                            continue
                        
                        # Hedef durumlar ayırt edilebilir mi?
                        ti_idx = self.state_index[ti]
                        tj_idx = self.state_index[tj]
                        
                        if self._is_distinguishable(ti_idx, tj_idx):
                            self._mark_distinguishable(i, j, f"δ({si},{symbol})={ti}, δ({sj},{symbol})={tj}")
                            marked_this_round.append({
                                'pair': (si, sj),
                                'symbol': symbol,
                                'targets': (ti, tj)
                            })
                            changed = True
                            break
            
            if marked_this_round:
                step_info = {
                    'type': 'iteration',
                    'step': iteration,
                    'description': f"İterasyon {iteration - 1}: Geçişler kontrol ediliyor.\n"
                                  f"İşaretlenen: {len(marked_this_round)} çift",
                    'marked_this_round': marked_this_round,
                    'partition': self._get_partition(),
                    'table': [row[:] for row in self.table]
                }
                self.steps.append(step_info)
                yield step_info
                iteration += 1
        
        # Final partition
        self.partition = self._get_partition()
        
        # Minimize edilmiş DFA'yı oluştur
        minimized_dfa = self._build_minimized_dfa()
        
        step_info = {
            'type': 'final',
            'step': iteration,
            'description': f"Minimizasyon tamamlandı!\n"
                          f"Orijinal durum sayısı: {len(self.dfa.states)}\n"
                          f"Minimize edilmiş durum sayısı: {len(minimized_dfa.states)}\n"
                          f"Final partition: {[sorted(g) for g in self.partition]}",
            'partition': self.partition,
            'table': [row[:] for row in self.table],
            'minimized_states': len(minimized_dfa.states)
        }
        self.steps.append(step_info)
        yield step_info
        
        return minimized_dfa
    
    def _build_minimized_dfa(self) -> DFA:
        """Partition'dan minimize edilmiş DFA oluştur"""
        # Her grup için temsilci seç
        state_to_group: Dict[str, int] = {}
        group_representatives: Dict[int, str] = {}
        
        for i, group in enumerate(self.partition):
            sorted_group = sorted(group)
            representative = sorted_group[0]
            group_representatives[i] = representative
            for state in group:
                state_to_group[state] = i
        
        # Yeni durum isimleri
        new_states = set()
        new_transitions = {}
        new_accept = set()
        
        for i, group in enumerate(self.partition):
            new_state = f"q{i}"
            new_states.add(new_state)
            
            # Kabul durumu mu?
            if group & self.dfa.accept_states:
                new_accept.add(new_state)
            
            # Geçişler
            representative = group_representatives[i]
            new_transitions[new_state] = {}
            
            for symbol in self.dfa.alphabet:
                target = self.dfa.transition(representative, symbol)
                if target:
                    target_group = state_to_group[target]
                    new_transitions[new_state][symbol] = f"q{target_group}"
        
        # Başlangıç durumu
        start_group = state_to_group[self.dfa.start_state]
        new_start = f"q{start_group}"
        
        return DFA(
            states=new_states,
            alphabet=self.dfa.alphabet.copy(),
            transitions=new_transitions,
            start_state=new_start,
            accept_states=new_accept
        )
    
    def minimize(self) -> DFA:
        """DFA'yı minimize et (adım adım takip etmeden)"""
        result = None
        for step in self.minimize_full():
            pass
        return self._build_minimized_dfa()
    
    def get_table_display(self) -> str:
        """Tabloyu string olarak göster"""
        if self.n == 0:
            return "Boş tablo"
        
        # Başlık
        lines = ["     " + "  ".join(f"{s:>4}" for s in self.states[:-1])]
        
        # Satırlar
        for i in range(1, self.n):
            row = f"{self.states[i]:>4} "
            cells = []
            for j in range(i):
                val = self._is_distinguishable(j, i)
                if val is True:
                    cells.append("  X ")
                elif val is False:
                    cells.append("  - ")
                else:
                    cells.append("  ? ")
            row += "  ".join(cells)
            lines.append(row)
        
        return "\n".join(lines)
    
    def get_all_steps(self) -> List[dict]:
        """Tüm adımları döndür"""
        return self.steps


def minimize_dfa(dfa: DFA) -> Tuple[DFA, List[dict]]:
    """
    Convenience function: DFA'yı minimize et
    
    Args:
        dfa: Minimize edilecek DFA
        
    Returns:
        (Minimize edilmiş DFA, adımlar listesi)
    """
    minimizer = DFAMinimization(dfa)
    minimized = minimizer.minimize()
    return minimized, minimizer.get_all_steps()
