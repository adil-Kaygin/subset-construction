# 🔄 Finite Automata Toolkit

BIL 334 - Otomata Teorisi için geliştirilen interaktif sonlu otomat araç seti.

## 📚 Özellikler

| Modül | Açıklama |
|-------|----------|
| **JSON Creator (GUI)** | İnteraktif GUI ile NFA/DFA oluşturma ve JSON çıktısı |
| **Lazy Subset Construction** | NFA → DFA dönüşümü (adım adım görselleştirme) |
| **DFA Minimization** | Table-Filling algoritması ile DFA minimizasyonu |
| **Regex → ε-NFA** | Thompson Construction algoritması |
| **DFA Karşılaştırma** | İki DFA'nın eşdeğerlik kontrolü |

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Graphviz (sistem paketi)

### Adımlar

1. **Graphviz'i yükleyin** (sistem paketi olarak):

```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# macOS
brew install graphviz

# Windows
choco install graphviz
```

2. **Python bağımlılıklarını yükleyin**:

```bash
cd subset-construction
pip install -r requirements.txt
```

3. **Uygulamayı çalıştırın**:

```bash
streamlit run app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde açılacaktır.

## 📝 Veri Formatı

### NFA JSON Formatı

```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"a": ["q0", "q1"], "b": ["q0"], "ε": ["q2"]},
    "q1": {"b": ["q2"]},
    "q2": {}
  },
  "start_state": "q0",
  "accept_states": ["q2"]
}
```

### DFA JSON Formatı

```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"a": "q1", "b": "q0"},
    "q1": {"a": "q1", "b": "q2"},
    "q2": {"a": "q1", "b": "q0"}
  },
  "start_state": "q0",
  "accept_states": ["q2"]
}
```

**Not:** 
- NFA'da geçişler liste olarak tanımlanır (`["q0", "q1"]`)
- DFA'da geçişler tek durum olarak tanımlanır (`"q1"`)
- Epsilon geçişleri için `"ε"` sembolünü kullanın

## 📖 Modül Açıklamaları

### 🎨 JSON Creator (GUI)

**İnteraktif Finite Automata Builder**

Queue-based yaklaşım ile adım adım NFA veya DFA oluşturun.

**Özellikler:**
- Otomata tipi seçimi (NFA/DFA)
- Alfabe tanımlama
- Kuyruk tabanlı durum işleme
- Geçiş tanımlama ve doğrulama
- Kabul durumu işaretleme
- Otomatik JSON çıktısı oluşturma
- Görselleştirme ve doğrulama
- JSON indirme

**Adımlar:**
1. Otomata tipi seçin (NFA/DFA)
2. Alfabeyi tanımlayın
3. Başlangıç durumunu ayarlayın (kuyruğa eklenir)
4. Kuyruktaki durumları sırayla işleyin
5. Geçişleri tanımlayın ve yeni durumları kuyruğa ekleyin
6. Kabul durumlarını işaretleyin
7. JSON çıktısını oluşturun ve indirin

### 1️⃣ NFA → DFA (Lazy Subset Construction)

**Lazy Subset Construction** algoritması, klasik subset construction'dan farklı olarak sadece gerekli durumları "lazy" (tembel) şekilde hesaplar.

**Özellikler:**
- Adım adım görselleştirme
- Her adımda NFA ve DFA grafikleri
- Epsilon kapanışı hesaplamaları
- JSON çıktısı ve indirme

### 2️⃣ DFA Minimization

**Table-Filling** (Myhill-Nerode) algoritması ile DFA minimizasyonu.

**Algoritma:**
1. Kabul ve red durumlarını ayır (temel durum)
2. İteratif olarak ayırt edilebilir çiftleri işaretle
3. Ayırt edilemeyen durumları birleştir

**Özellikler:**
- Renkli partition görselleştirmesi
- Ayırt edilebilirlik tablosu
- Orijinal ve minimize durum karşılaştırması

### 3️⃣ Regex → ε-NFA (Thompson Construction)

**Thompson Construction** algoritması ile regex'i ε-NFA'ya dönüştürür.

**Desteklenen Operatörler:**
| Operatör | Açıklama | Öncelik |
|----------|----------|---------|
| `(...)` | Gruplama | En yüksek |
| `*` | Kleene Star (0 veya daha fazla) | Yüksek |
| `+` | Kleene Plus (1 veya daha fazla) | Yüksek |
| `?` | Optional (0 veya 1) | Yüksek |
| `ab` | Concatenation | Orta |
| `a\|b` | Union | Düşük |

**Örnekler:**
- `a*b` → 0 veya daha fazla 'a', ardından 'b'
- `(a|b)*` → 'a' veya 'b' karakterlerinden oluşan herhangi bir string
- `(ab)+` → bir veya daha fazla "ab" tekrarı

### 4️⃣ DFA Karşılaştırma

İki DFA'nın aynı dili kabul edip etmediğini kontrol eder.

**Yöntem:** Symmetric Difference
- L(A) △ L(B) = (L(A) - L(B)) ∪ (L(B) - L(A))
- Eğer L(A) △ L(B) = ∅ ise, DFA'lar eşdeğerdir

**Özellikler:**
- Karşı örnek bulma
- Alt küme ilişkisi kontrolü
- String testi

## 📁 Proje Yapısı

```
subset-construction/
├── app.py                    # Streamlit ana uygulama
├── requirements.txt          # Python bağımlılıkları
├── README.md                 # Bu dosya
├── automata/
│   ├── __init__.py
│   ├── nfa.py               # NFA veri yapısı
│   ├── dfa.py               # DFA veri yapısı
│   ├── visualizer.py        # Graphviz görselleştirme
│   ├── lazy_subset.py       # Lazy Subset Construction
│   ├── minimization.py      # DFA Minimization
│   ├── regex_to_nfa.py      # Regex → ε-NFA
│   └── comparison.py        # DFA Comparison
├── examples/
│   ├── nfa_example1.json
│   ├── nfa_epsilon.json
│   └── dfa_example1.json
└── output/                  # Oluşturulan grafikler
```

## 🧪 Örnek Kullanım (Programatik)

```python
from automata import NFA, DFA
from automata.lazy_subset import LazySubsetConstruction
from automata.minimization import DFAMinimization
from automata.regex_to_nfa import RegexToNFA
from automata.comparison import DFAComparison

# NFA'dan DFA'ya dönüşüm
nfa = NFA.from_json_file("examples/nfa_example1.json")
converter = LazySubsetConstruction(nfa)
dfa = converter.convert()
print(f"DFA durumları: {dfa.states}")

# DFA Minimization
minimizer = DFAMinimization(dfa)
minimized = minimizer.minimize()
print(f"Minimize durumları: {minimized.states}")

# Regex → ε-NFA
regex_converter = RegexToNFA()
epsilon_nfa = regex_converter.convert("(a|b)*abb")
print(f"ε-NFA durumları: {epsilon_nfa.states}")

# DFA Karşılaştırma
comparator = DFAComparison(dfa1, dfa2)
is_equivalent, steps = comparator.are_equivalent()
print(f"Eşdeğer mi: {is_equivalent}")
```

## 📄 Lisans

Bu kod eğitim amaçlıdır, hatalar içerebilir, lütfen kendi kontrollerinizi yapın

## 👤 Geliştirici

Claude 4.5 Opus
