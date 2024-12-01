#lang racket

;; A Posn is a (posn Num Num)
(struct posn (x y))

;; A Rope is a (rope Posn Posn)
(struct rope (head tail))

;; Posn Posn --> Boolean
(define (posn=? p1 p2)
  (and (= (posn-x p1) (posn-x p2))
       (= (posn-y p1) (posn-y p2))))

;; Posn Char --> Posn
(define (move-posn p instr)
  (cond [(char=? instr #\R) (posn (add1 (posn-x p)) (posn-y p))]
        [(char=? instr #\L) (posn (sub1 (posn-x p)) (posn-y p))]
        [(char=? instr #\U) (posn (posn-x p) (add1 (posn-y p)))]
        [(char=? instr #\D) (posn (posn-x p) (sub1 (posn-y p)))]))

;; Posn Posn --> Number
(define (x-diff p1 p2)
  (- (posn-x p1) (posn-x p2)))

;; Posn Posn --> Number
(define (y-diff p1 p2)
  (- (posn-y p1) (posn-y p2)))

;; Posn Posn --> Unit-Posn
(define (get-move head tail)
  (posn (move-x head tail) (move-y head tail)))

;; Posn Posn --> Number
(define (move-x head tail)
  (cond [(touching? head tail) 0]
        [(and (= (abs (x-diff head tail)) 2)
              (= (abs (y-diff head tail)) 0))
         (/ (x-diff head tail) (abs (x-diff head tail)))]
        [(and (not (= (posn-x head) (posn-x tail)))
              (not (= (posn-y head) (posn-y tail))))
         (/ (x-diff head tail) (abs (x-diff head tail)))]
        [else 0]))

;; Posn Posn --> Number
(define (move-y head tail)
  (cond [(touching? head tail) 0]
        [(and (= (abs (y-diff head tail)) 2)
              (= (abs (x-diff head tail)) 0))
         (/ (y-diff head tail) (abs (y-diff head tail)))]
        [(and (not (= (posn-x head) (posn-x tail)))
              (not (= (posn-y head) (posn-y tail))))
         (/ (y-diff head tail) (abs (y-diff head tail)))]
        [else 0]))

;; Posn Posn --> Bool
(define (touching? p1 p2)
  (and (<= (abs (x-diff p1 p2)) 1)
       (<= (abs (y-diff p1 p2)) 1)))

;; Rope Symbol --> Rope
(define (move-head r instr)
  (rope (move-posn (rope-head r) instr) (rope-tail r)))

;; Rope --> Rope
(define (move-tail r)
  (let ([move (get-move (rope-head r) (rope-tail r))])
    (rope
     (rope-head r)
     (posn (+ (posn-x move) (posn-x (rope-tail r)))
           (+ (posn-y move) (posn-y (rope-tail r)))))))

;; Rope --> Rope
(define (move-rope r instr)
  (move-tail (move-head r instr)))

;; String --> ListOf Symbol
(define (parse-input str)
  (foldr append '() (map normalize-input (string-split str "\n"))))

;; String --> LoSymbol
(define (normalize-input str)
  (let ([dir (string-ref str 0)]
        [num (string->number (substring str 2))])
    (build-list num (λ(x) dir))))


;; LoSymbol --> Number
(define (eval-spaces dirs)
  (length (remove-duplicates
           (eval-spaces-help
            dirs
            (rope (posn 0 0) (posn 0 0))
            (list (posn 0 0)))
           posn=?)))

;; LoSymbol Rope [HashTable Posn --> Boolean] --> ListOf Posn
(define (eval-spaces-help dirs r lop)
  (cond [(empty? dirs) lop]
        [(cons?  dirs)
         (let ([new-rope (move-rope r (first dirs))])
           (eval-spaces-help
            (rest dirs)
            new-rope
            (cons (rope-tail new-rope) lop)))]))

;; String --> Number
(define (count-spaces str)
  (eval-spaces (parse-input str)))



(define (print-rope r)
  (let ([out (string-append
              "(" (number->string (posn-x (rope-tail r))) ", "
              (number->string (posn-y (rope-tail r))) ") --> "
              "(" (number->string (posn-x (rope-head r))) ", "
              (number->string (posn-y (rope-head r))) ")")])
    (println out)))


(define (print-posn p)
  (println (string-append
            "(" (number->string (posn-x p)) ", " (number->string (posn-y p)) ")")))

;; ====================================================

;; TODO: replace rope struct with [List-of Posn]
;; Propagate movements using a fold

(define test* (list
               (posn 4 0)
               (posn 3 0)
               (posn 2 0)
               (posn 1 0)
               (posn 0 0)))

;; LoPosn Char --> LoPosn
;; Assumes that |lop| >= 2
(define (move-rope* lop dir)
  (let ([new-head (move-posn (first lop) dir)])
    (foldl
     (λ(knot moved)
       (append moved
               (list
                (rope-tail
                 (move-tail
                  (rope (last moved) knot))))))
     (list new-head)
     (rest lop))))

;; String --> Number
(define (count-spaces* str)
  (length
   (remove-duplicates
           (eval-rope*
            (build-list 10 (λ(x) (posn 0 0)))
            (parse-input str)
            '())
           posn=?)))

;; LoPosn LoDir --> LoPosn
(define (eval-rope* lop dir visited)
  (cond [(empty? dir) visited]
        [(cons? dir)
         (let ([new-rope (move-rope* lop (first dir))])
           (eval-rope* new-rope (rest dir) (cons (last new-rope) visited)))]))








