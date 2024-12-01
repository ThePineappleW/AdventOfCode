;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-advanced-reader.ss" "lang")((modname day1) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #t #t none #f () #f)))
(require racket/list)

;; String --> Num
(define (max-cals input) (list-max (group-calories-sums input)))

;; String --> Num
(define (top3sum input) (list-max-three (group-calories-sums input)))

;; LoNum --> Num
(define (list-max-three lst) (list-sum (take (sort lst >) 3)))

;; String --> [List-of Number]
(define (group-calories-sums input)
  (map list-sum (map los->lon (lostr->lolon (loc->str (string->list input) "" '())))))

;; X [List-of X] --> [List-of X]
(define (add-to-last x lox op)
  (cond [(empty? lox) (list x)]
        [(cons? lox) (reverse (cons (op x (last lox)) (rest (reverse lox))))]))

;; LoNum --> Num
(define (list-max lon) (foldr max 0 lon))

;; LoNum --> Num
(define (list-sum lon) (foldr + 0 lon))

;; LoString --> LoNum
(define (los->lon los) (map string->number los))

;; LoString --> LoLoNumber
(define (lostr->lolon lostr)
  (foldr (λ(s acc)
           (if (not (string=? "" s))
               (add-to-last s acc cons)
               (append acc '(()))))
         '(()) lostr))

;; LoChar String LoString--> LoString
(define (loc->str loc curString acc)
  (cond [(empty? loc) acc]
        [(char=? #\newLine (first loc)) (loc->str (rest loc) "" (cons curString acc))]
        [else (loc->str (rest loc) (string-append curString (string (first loc))) acc)]))