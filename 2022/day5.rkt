;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-intermediate-lambda-reader.ss" "lang")((modname day5) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require racket/base)
(require racket/list)
(require racket/string)

(define-struct instr (quant from to))
(define-struct crates (cols))

;; Manual entry because it was faster than writing a parser.
;; That would be fairly straightforward with regexps after splitting into lines,
;; i.e. to get column n, match all letters preceded by 3(n-1) + n + 1 (or so) characters.
(define INIT-CRATES
  (make-crates
   '((V R H B G D W)
     (F R C G N J)
     (J N D H F S L)
     (V S D J)
     (V N W Q R D H S)
     (M C H G P)
     (C H Z L G B J F)
     (R J S)
     (M V N B R S G L))))

(define TEST-CRATES
  (make-crates
   '((N Z)
     (D C M)
     (P)
     )))

;; Crates String --> String
(define (reveal-answer crates str)
  (read-first-letters (crates-cols (move-all-crates crates str))))

;; LoLoSymbol --> String
(define (read-first-letters losym)
  (foldr (λ(col acc) (string-append (if (cons? col) (symbol->string (first col)) " ") acc)) "" losym))
  
;; Crates String --> Crates
(define (move-all-crates crates str)
  (foldl (λ(i c) (move-crates c i)) crates (parse-instrs str)))

;; String --> LoInstr
(define (parse-instrs str)
  (map (λ(i) (make-instr (string->number (first i)) (string->number (second i)) (string->number (third i))))
       (map (λ(x) (regexp-match* #rx"[0-9]+" x)) (string-split str "\n"))))

;; Crates --> Crates
(define (move-crates crates instr)
  (letrec ([from-idx (sub1 (instr-from instr))]
           [to-idx (sub1 (instr-to instr))]

           [from (list-ref (crates-cols crates) from-idx)]
         [to (list-ref (crates-cols crates) to-idx)]
         [taken (take-safe from (instr-quant instr))]
         ;; Part 1:
         ;; [inserted (append (reverse taken) to)]
         ;; Part 2:
         [inserted (append taken to)]
         ;; Could have done this as a boolean flag but I'm too lazy lol
         [remaining (list-tail-safe from (instr-quant instr))])
    (make-crates
     (replace-index
      from-idx
      remaining
      (replace-index to-idx inserted (crates-cols crates))))))

;; LoX Num X --> LoX
(define (replace-index i x lox)
  (cond [(empty? lox) lox]
        [(and (cons? lox) (zero? i)) (cons x (rest lox))]
        [(cons? lox) (cons (first lox)(replace-index (sub1 i) x (rest lox)))]))

;; LoX --> LoX
(define (take-safe lst num) (if (>= (length lst) num) (take lst num) lst))

(define (list-tail-safe lst num) (if  (>= (length lst) num) (list-tail lst num) lst))

