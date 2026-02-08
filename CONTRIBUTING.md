# 🤝 Katkıda Bulunma Rehberi

subset-construction projesine katkıda bulunmak istediğiniz için teşekkürler! Bu rehber, projeye nasıl katkıda bulunabileceğinizi açıklar.

## 📋 İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Geliştirme Ortamı Kurulumu](#geliştirme-ortamı-kurulumu)
- [Proje Yapısı](#proje-yapısı)
- [Katkı Süreci](#katkı-süreci)
- [Kod Standartları](#kod-standartları)
- [Issue'lar](#issuelar)

## 🎯 Proje Hakkında

Bu proje, **Otomata Teorisi** (BIL 334) dersi için geliştirilmiş interaktif bir finite automata araç setidir. Streamlit ile yazılmış bir web uygulaması olarak çalışır.

### Mevcut Özellikler

1. **JSON Creator** - NFA/DFA oluşturma arayüzü
2. **NFA → DFA** - Lazy Subset Construction algoritması
3. **DFA Minimization** - Table-Filling algoritması
4. **Regex → ε-NFA** - Thompson Construction
5. **DFA Karşılaştırma** - İki DFA'nın eşdeğerlik kontrolü

### Açık İssue'lar

Katkıda bulunabileceğiniz issue'lar için [Issues sayfasına](https://github.com/adil-Kaygin/subset-construction/issues) bakın. `good first issue` ve `help wanted` etiketli issue'lar başlangıç için uygundur.

## 🛠️ Geliştirme Ortamı Kurulumu

### Gereksinimler

- Python 3.8 veya üzeri
- Graphviz (sistem paketi)
- Git

### Kurulum Adımları

1. **Repository'yi fork edin**
   - GitHub'da sağ üstteki "Fork" butonuna tıklayın

2. **Yerel kopya oluşturun**
   ```bash
   git clone https://github.com/KULLANICI_ADINIZ/subset-construction.git
   cd subset-construction
   ```

3. **Graphviz'i yükleyin**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install graphviz
   
   # macOS
   brew install graphviz
   
   # Windows
   choco install graphviz
   ```

4. **Python sanal ortamı oluşturun (önerilir)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

5. **Bağımlılıkları yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

6. **Uygulamayı çalıştırın**
   ```bash
   streamlit run app.py
   ```
   
   Tarayıcınızda `http://localhost:8501` açılacaktır.

## 📁 Proje Yapısı

```
subset-construction/
├── app.py                    # Ana Streamlit uygulaması
├── requirements.txt          # Python bağımlılıkları
├── README.md                 # Proje dokümantasyonu
├── CONTRIBUTING.md           # Bu dosya
├── automata/                 # Automata modülleri
│   ├── __init__.py
│   ├── nfa.py               # NFA veri yapısı ve operasyonları
│   ├── dfa.py               # DFA veri yapısı ve operasyonları
│   ├── visualizer.py        # Graphviz ile görselleştirme
│   ├── lazy_subset.py       # NFA → DFA dönüşümü
│   ├── minimization.py      # DFA minimizasyonu
│   ├── regex_to_nfa.py      # Regex → ε-NFA dönüşümü
│   └── comparison.py        # DFA karşılaştırma
├── examples/                 # Örnek automata JSON dosyaları
│   ├── nfa_example1.json
│   ├── nfa_epsilon.json
│   └── dfa_example1.json
└── .github/
    └── ISSUE_TEMPLATE/       # Issue şablonları
```

### Modül Açıklamaları

#### `automata/nfa.py` ve `automata/dfa.py`

Bu dosyalar temel veri yapılarını içerir:
- Durum, alfabe, geçiş fonksiyonu
- JSON import/export
- Temel operasyonlar (accepts, etc.)

#### `automata/visualizer.py`

Graphviz kullanarak automata görselleştirmesi yapar. Hem NFA hem DFA için çalışır.

#### `automata/lazy_subset.py`

Lazy Subset Construction algoritması - NFA'yı DFA'ya dönüştürür. "Lazy" yaklaşım, sadece erişilebilir durumları hesaplar.

#### `automata/minimization.py`

Table-Filling (Myhill-Nerode) algoritması ile DFA minimizasyonu.

#### `automata/regex_to_nfa.py`

Thompson Construction algoritması - Regular Expression'ı epsilon-NFA'ya dönüştürür.

#### `automata/comparison.py`

İki DFA'nın eşdeğerlik kontrolü - Symmetric Difference yöntemi.

#### `app.py`

Streamlit tabanlı web arayüzü. Tüm modülleri birleştirip kullanıcı dostu bir interface sunar.

## 🔄 Katkı Süreci

### 1. Issue Seçimi veya Oluşturma

- Mevcut issue'lardan birini seçin veya yeni bir issue açın
- Issue'yu kendinize assign edin (maintainer'lar atayacaktır)
- Tartışmalar için issue altına yorum yazın

### 2. Branch Oluşturma

```bash
# Ana repository'den güncel kodları çekin
git checkout main
git pull upstream main  # upstream'i ilk seferde ekleyin

# Yeni feature branch oluşturun
git checkout -b feature/issue-aciklamasi
```

Branch isimlendirme:
- `feature/regex-comparison` - Yeni özellik
- `fix/bug-aciklamasi` - Bug düzeltmesi
- `docs/dokumasyon-guncelleme` - Dokümantasyon

### 3. Kod Yazma

- Küçük, atomik commit'ler yapın
- Her commit anlamlı bir değişiklik içermeli
- Commit mesajları açıklayıcı olmalı

```bash
git add .
git commit -m "feat: RE karşılaştırma paneli UI eklendi"
```

Commit mesaj formatı:
- `feat:` - Yeni özellik
- `fix:` - Bug düzeltmesi
- `docs:` - Dokümantasyon değişikliği
- `refactor:` - Kod iyileştirmesi
- `test:` - Test ekleme/düzenleme

### 4. Test Etme

- Değişikliklerinizi manuel olarak test edin
- Streamlit uygulamasını çalıştırıp her özelliği kontrol edin
- Edge case'leri test edin

```bash
streamlit run app.py
```

### 5. Pull Request Açma

```bash
# Fork'unuza push edin
git push origin feature/issue-aciklamasi
```

GitHub'da:
1. "Pull Request" butonuna tıklayın
2. Başlık ve açıklama ekleyin
3. İlgili issue'yu referans verin (örn: "Closes #5")
4. Değişikliklerinizi özetleyin

#### PR Açıklama Şablonu

```markdown
## Açıklama
Bu PR, [issue numarası] için [özellik/düzeltme] ekler.

## Değişiklikler
- [ ] Yeni modül: `automata/yeni_modul.py`
- [ ] UI güncellemesi: `app.py`
- [ ] Dokümantasyon güncellemesi

## Test
- [ ] Manuel olarak test edildi
- [ ] Edge case'ler kontrol edildi
- [ ] Mevcut özellikler çalışıyor

## Ekran Görüntüleri (varsa)
[Görsel ekleyin]

## Checklist
- [ ] Kod temiz ve okunabilir
- [ ] Yorum satırları eklendi (gerektiğinde)
- [ ] README güncellenmiş (gerekirse)
```

## 📝 Kod Standartları

### Python Stil Rehberi

- PEP 8 standartlarına uyun (mümkün olduğunca)
- Fonksiyon ve sınıflar için docstring yazın
- Değişken isimleri açıklayıcı olmalı

```python
def eliminate_state(self, state: str) -> None:
    """
    Bir durumu elimine et ve regex'leri güncelle
    
    Args:
        state: Elimine edilecek durum
        
    Returns:
        None
    """
    # Implementasyon
    pass
```

### Türkçe/İngilizce Kullanımı

- Kod içi değişken, fonksiyon isimleri: İngilizce
- Docstring'ler: Türkçe (eğitim projesi olduğu için)
- Yorumlar: Türkçe veya İngilizce (tercihe göre)
- UI metinleri: Türkçe

### Modülerlik

- Her özellik kendi modülünde olmalı
- `app.py` sadece UI ve orchestration için kullanılmalı
- Algoritmalar `automata/` dizininde olmalı

## 🐛 Issue'lar

### Yeni Issue Açma

Issue açmadan önce:
1. Mevcut issue'lara bakın (duplicate olmasın)
2. README'yi okuyun
3. Uygun template kullanın

Issue tipleri:
- **Bug Report**: Bir hata bulduysanız
- **Feature Request**: Yeni özellik önerisi
- **Question**: Genel sorular

### Good First Issue

Yeni başlayanlar için uygun issue'lar `good first issue` etiketi ile işaretlenir. Bunlar:
- Küçük kapsamlı değişiklikler
- İyi dokümante edilmiş
- Belirgin kabul kriterleri var

## 🎓 Öğrenme Kaynakları

Otomata teorisi hakkında bilginiz yoksa:

- **Kitap**: Michael Sipser - "Introduction to the Theory of Computation"
- **Video**: [Stanford CS154 - Automata Theory](https://www.youtube.com/playlist?list=PLoCMsyE1cvdWiqJ6qjaqfTVzP1sXGN7ot)
- **Online**: [Automata Theory Tutorial](https://www.tutorialspoint.com/automata_theory/index.htm)

## ❓ Sorular

Sorularınız varsa:
- Issue altında yorum yapın
- GitHub Discussions kullanın
- README'de bulunan bilgilere bakın

## 🙏 Teşekkürler

Projeye katkıda bulunmayı düşündüğünüz için teşekkürler! Her katkı değerlidir - büyük veya küçük fark etmez.

Happy Coding! 🚀
