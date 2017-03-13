# Lokalizacja znaczników QR

#  Wizja
## 1. Wstęp
Celem projektu jest stworzenie systemu nawigacji robota z użyciem znaczników rozmieszczonych na wyznaczonym obszarze.
Znaczniki to kody QR, które z użyciem kamery zainstalowanej na robocie pozwolą na określenie aktualnej pozycji.
Robot za pośrednictwem kamery będzie pobierał obraz swojego otoczenia, następnie przekazywał go do programu uruchomionego na komputerze pokładowym. Program zaimplementowany z użyciem bibliotek do rozpoznawania obrazu dokonywać będzie detekcji kodów QR.
Po zidentyfikowaniu kodu robot odszukuje danych na jego temat w pliku typu JSON z informacjami o istotnych dla systemu elementach budynku, dzięki czemu określa swoje aktualne położenie.

## 2. Zadania do zrealizowania:
1) Zaimplementowanie detekcji kodów QR z użyciem kamery - znalezienie biblioteki do rozpoznawania obrazów, znalezienie istniejących rozwiązań problemu (detekcji kodów QR), przetestowanie skuteczności wykrywania kodów w zależności od odległości od kamery i kąta widzenia
2) Dostosowanie programu do możliwości obliczeniowych PandaBoard sterującego robotem - w oparciu o istniejące rozwiązania, zaimplementowanie programu wykrywającego w dostarczonym z kamery obrazie kod QR
3) Rozszerzenie formatu pliku JSON opisującego budynek o informację na temat kodu QR 
4) Implementacja programu do wyszukania informacji o kodzie QR w pliku JSON opisującym budynek
5) Opracowanie algorytmu przemieszczania się robota z punktu A do B z użyciem kodów QR
6) Zwiększenie pola widzenia kamery poprzez umieszczenie jej na głowicy obrotowej, uwzględnienie zmian w implementacji programów

## 3. Informacje szczegółowe
1) Wykorzystywana kamera
Zespół dysponuje kamerą o wysokiej rozdzielczości i szerokim kącie widzenia.  
Do rozważenia pozostaje kwestia konieczności zwiększenia pola widzenia robota poprzez zastosowanie większej liczby kamer lub 
umieszczenie kamery na obrotowej głowicy. Problemem może okazać się skuteczność wykrywania kodów QR z użyciem wspomnianej kamery 
i biblioteki zależna głównie od odległości znacznika od kamery oraz kąta widzenia.

2) Biblioteka do rozpoznawania kodów QR
Jako biblioteki do rozpoznawania kodów QR użyjemy biblioteki openCV, opierając się na istniejącej implementacji detekrora kodów QR:
https://github.com/bharathp666/opencv_qr
Implementacja zostanie dostosowana do możliwości obliczeniowych komputera używanego w robocie.

3) Detekcja pozycji kodów QR
Do detekcji dokładnej pozycji kodów spróbujemy użyć istniejących do tego bibliotek i na ich podstawie stworzyć algorytm pokazujący, 
w jakim stosunku do naszego robota się on znajduje. Dzięki temu mając bazę rozmieszczeń kodów QR będziemy mogli ustalić dość 
dokładną pozycję naszego obiektu.

4) Robot
Zespół otrzymuje do dyspozycji robota czterokołowego sterowanego z użyciem PandaBoard. 
https://capo.iisg.agh.edu.pl/doku.php/robot  

Mail autorów pracy magisterskiej związanej z projektem: suwala@student.agh.edu.pl
Przydatne linki: http://home.agh.edu.pl/~wojturek/dokuwiki/doku.php?id=student:parm:start 

