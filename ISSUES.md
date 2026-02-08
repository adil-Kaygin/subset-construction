# 📋 Açık Issue'lar ve Katkı Fırsatları

Bu doküman, subset-construction projesine katkıda bulunmak isteyenler için mevcut issue'ları ve geliştirilmesi planlanan özellikleri açıklar.

## 🎯 Öncelikli Özellikler

### 1. 🔄 RE Karşılaştırma Paneli

**Issue Dosyası:** `.github/ISSUE_TEMPLATE/regex-comparison-panel.md`

**Amaç:** Kullanıcıların iki farklı Regular Expression girerek bunları DFA'ya dönüştürüp karşılaştırabilmelerini sağlamak.

**Dönüşüm Akışı:**
```
RE_1 → ε-NFA_1 → DFA_1
                            ↘
                              Karşılaştırma → Eşdeğerlik Sonucu
                            ↗
RE_2 → ε-NFA_2 → DFA_2
```

**Zorluk Seviyesi:** 🟢 Kolay-Orta (Good First Issue)

**Neden Kolay:**
- Mevcut modüller zaten var (`regex_to_nfa.py`, `lazy_subset.py`, `comparison.py`)
- Sadece bunları birleştirip UI oluşturmak gerekiyor
- İyi dokümante edilmiş

**Ne Yapılacak:**
1. `app.py`'ye yeni bir menü seçeneği ekle (5️⃣ RE Karşılaştırma)
2. İki text input alanı oluştur (RE_1 ve RE_2 için)
3. Dönüşüm adımlarını görselleştir
4. Karşılaştırma sonuçlarını göster

**Gerekli Bilgiler:**
- Streamlit kullanımı (örnekler `app.py`'de mevcut)
- Thompson Construction (mevcut: `regex_to_nfa.py`)
- Lazy Subset Construction (mevcut: `lazy_subset.py`)
- DFA Comparison (mevcut: `comparison.py`)

---

### 2. 🔀 NFA/DFA → RE Dönüşümü

**Issue Dosyası:** `.github/ISSUE_TEMPLATE/automata-to-regex.md`

**Amaç:** Bir finite automata (NFA veya DFA) verildiğinde, bu otomatın kabul ettiği dili temsil eden Regular Expression'ı bulmak.

**Dönüşüm Akışı:**
```
NFA/DFA → State Elimination Algoritması → Regular Expression
```

**Zorluk Seviyesi:** 🟡 Orta-Zor (Challenging)

**Neden Zor:**
- Yeni bir algoritma implementasyonu gerekiyor (State Elimination)
- Regex manipülasyonu ve simplification
- Daha kompleks matematiksel mantık

**Ne Yapılacak:**
1. Yeni modül oluştur: `automata/automata_to_regex.py`
2. State Elimination algoritmasını implementa et
3. `app.py`'ye yeni menü seçeneği ekle
4. Adım adım görselleştirme ekle

**Algoritma: State Elimination**

Basit açıklama:
1. Otomata tek başlangıç ve tek kabul durumuna sahip olmalı
2. Diğer durumları teker teker elimine et
3. Her eliminasyon sırasında geçiş etiketlerini regex olarak birleştir
4. Sonunda sadece: `[start] --regex--> [accept]` kalır

**Gerekli Bilgiler:**
- State Elimination algoritması
- Regex syntax ve manipülasyon
- NFA/DFA yapıları (mevcut: `nfa.py`, `dfa.py`)
- Graphviz görselleştirme (mevcut: `visualizer.py`)

---

## 🗺️ Genel Proje Mimarisi

### Mevcut Modüller

```
automata/
├── nfa.py              - NFA veri yapısı
├── dfa.py              - DFA veri yapısı
├── visualizer.py       - Graphviz ile görselleştirme
├── lazy_subset.py      - NFA → DFA (Lazy Subset Construction)
├── minimization.py     - DFA Minimization (Table-Filling)
├── regex_to_nfa.py     - RE → ε-NFA (Thompson Construction)
└── comparison.py       - DFA Comparison (Symmetric Difference)
```

### Nasıl Çalışır?

#### 1. Veri Yapıları (`nfa.py`, `dfa.py`)

Automata'lar sınıf olarak temsil edilir:

```python
class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states          # Set of states
        self.alphabet = alphabet      # Input alphabet
        self.transitions = transitions # Transition function (dict)
        self.start_state = start_state
        self.accept_states = accept_states
```

JSON formatı:
```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"a": ["q0", "q1"], "ε": ["q1"]},
    "q1": {"b": ["q1"]}
  },
  "start_state": "q0",
  "accept_states": ["q1"]
}
```

#### 2. Algoritmalar

Her algoritma kendi modülünde:

**Lazy Subset Construction** (`lazy_subset.py`):
- Input: NFA
- Output: DFA
- Metod: `LazySubsetConstruction(nfa).convert()`

**Thompson Construction** (`regex_to_nfa.py`):
- Input: Regex string
- Output: ε-NFA
- Metod: `RegexToNFA().convert("(a|b)*")`

**DFA Minimization** (`minimization.py`):
- Input: DFA
- Output: Minimized DFA
- Metod: `DFAMinimization(dfa).minimize()`

**DFA Comparison** (`comparison.py`):
- Input: DFA_1, DFA_2
- Output: Eşdeğer mi? + Karşı örnek
- Metod: `DFAComparison(dfa1, dfa2).are_equivalent()`

#### 3. UI (`app.py`)

Streamlit kullanarak modülleri birleştirir:

```python
# Menü seçimi
menu_option = st.sidebar.radio("İşlem Seçin:", [
    "🏠 Ana Sayfa",
    "1️⃣ NFA → DFA",
    "2️⃣ DFA Minimization",
    # ...
])

# Her menü için farklı sayfa
if menu_option == "1️⃣ NFA → DFA":
    # NFA input
    nfa_json = st.text_area("NFA JSON")
    nfa = NFA.from_json(json.loads(nfa_json))
    
    # Dönüşüm
    converter = LazySubsetConstruction(nfa)
    dfa = converter.convert()
    
    # Görselleştirme
    show_dfa_graph(dfa)
```

---

## 🚀 Nasıl Başlanır?

### Yeni Başlayanlar İçin: RE Karşılaştırma

1. **Projeyi klonla ve çalıştır**
   ```bash
   git clone https://github.com/adil-Kaygin/subset-construction.git
   cd subset-construction
   pip install -r requirements.txt
   streamlit run app.py
   ```

2. **Mevcut özellikleri incele**
   - "3️⃣ Regex → ε-NFA" menüsüne bak
   - "4️⃣ DFA Karşılaştırma" menüsüne bak
   - Nasıl çalıştıklarını anla

3. **Kodu incele**
   - `automata/regex_to_nfa.py` - Regex'i nasıl parse ediyor?
   - `automata/comparison.py` - DFA'ları nasıl karşılaştırıyor?
   - `app.py` satır 350-450 arası - Streamlit UI nasıl yazılmış?

4. **Yeni özellik ekle**
   - `app.py`'de yeni menü seçeneği ekle
   - İki regex input alanı oluştur
   - Mevcut modülleri çağır
   - Sonuçları göster

### Deneyimliler İçin: NFA/DFA → RE

1. **Algoritma araştırması**
   - State Elimination algoritmasını öğren
   - Örnekleri elle çöz (kağıt-kalem)
   - Pseudocode yaz

2. **Implementasyon**
   - `automata/automata_to_regex.py` oluştur
   - Temel sınıf ve metodları yaz
   - Adım adım test et

3. **Görselleştirme**
   - Her eliminasyon adımını kaydet
   - Streamlit'te göster

4. **Edge case'ler**
   - Boş dil
   - Epsilon geçişleri
   - Self-loop'lar
   - Tek durum

---

## 📚 Yararlı Kaynaklar

### Otomata Teorisi
- [Stanford CS154](https://www.youtube.com/playlist?list=PLoCMsyE1cvdWiqJ6qjaqfTVzP1sXGN7ot)
- [MIT 6.045J](https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/)

### State Elimination
- [PDF Tutorial](https://web.stanford.edu/class/archive/cs/cs103/cs103.1142/lectures/18/Small18.pdf)
- [YouTube Açıklama](https://www.youtube.com/watch?v=--CSVsFIDng)

### Streamlit
- [Streamlit Docs](https://docs.streamlit.io/)
- `app.py` dosyasındaki örnekler

### Python
- Type hints kullanımı
- Dataclass'lar (isteğe bağlı)

---

## ✅ Checklist: Katkıda Bulunmadan Önce

- [ ] Projeyi yerel ortamda çalıştırdım
- [ ] Mevcut özellikleri test ettim
- [ ] İlgili issue'yu okudum
- [ ] CONTRIBUTING.md dosyasını okudum
- [ ] Hangi modülleri kullanacağımı biliyorum
- [ ] Gerekli algoritmaları anlıyorum

---

## 🤝 İletişim

- **Issue'lar:** Sorularınızı ilgili issue altında sorun
- **GitHub Discussions:** Genel tartışmalar için
- **Pull Request:** Kodunuzu gözden geçirmeliyiz

---

## 🎯 Hedef

Bu projenin amacı:
1. Otomata teorisini öğrenmek
2. Algoritmaları görselleştirerek anlamak
3. Açık kaynak katkısı yapmayı öğrenmek

Mükemmel kod beklemiyoruz - öğrenme süreci önemli! 🚀

**Katkılarınızı bekliyoruz!**
