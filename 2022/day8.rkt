#lang racket

(require racket/list)

;; A Tree is a (make-tree Num Bool Num)
(struct tree [height vis scenic])

;; A Forest is a LoLoTree

(define (print-tree t) (println (string-append (number->string (tree-height t)) ", " (if (tree-vis t) "#t" "#f") ", " (number->string (tree-scenic t)))))
(define (print-forest f) (map (λ(l) (map print-tree l)) f))
;; LoTree --> LoTree
(define (mark-all-vis-trees lotree)
  (cond [(empty? lotree) '()]
        [(cons?  lotree) (cons
                          (tree (tree-height (last lotree))
                                (if (visible? lotree) #t (tree-vis (last lotree)))
                                (tree-scenic (last lotree)))
                          (mark-all-vis-trees (reverse (rest (reverse lotree)))))]))

;; Tree --> Tree
(define (set-vis tree)
  (tree (tree-height tree) #t))

;; LoN --> Bool
;; Is the last element in this list visible?
(define (visible? trees)
  (if (<= (length trees) 1)
      #t
      (> (tree-height (last trees)) (apply max (map tree-height (rest (reverse trees)))))))

;; Forest --> Forest
(define (mark-visible forest)
  (map (compose reverse mark-all-vis-trees) forest))

;; Forest --> Forest
(define (rotate f) (map reverse (apply map list f)))

;; Forest --> Num
(define (count-visible/forest forest)
  (let ([count-vis/list (λ(lot) (foldr (λ(t acc) (if (tree-vis t) (add1 acc) acc)) 0 lot))])
    (foldr + 0 (map count-vis/list (mark-visible forest)))))
  
;; String --> Forest
(define (build-forest str)
  (let ([build-lot/str (λ(s) (map (λ(c) (tree (- (char->integer c) 48) #f 1)) (string->list s)))])
    (map build-lot/str (string-split str "\n"))))

;; Forest --> Forest
;; Accumulates the results of op on f rotated 0, 90, 180, and 270 degrees.
(define (rotate-reduce f op)
  (op (rotate (op (rotate (op (rotate (op f))))))))

(define (count-visible s)
  (let ([f (build-forest s)])
    (count-visible/forest (rotate-reduce f mark-visible))))

;; LoTree --> Num
;; Calculates the scenic value of the last tree in the list
(define (calc-scenic lotree)
  (letrec ([lot-rev (rest (reverse lotree))]
        [count-helper (λ(l acc)
                        (cond [(empty? l) acc]
                              [(>= (tree-height (first l)) (tree-height (last lotree))) (add1 acc)]
                              [else (count-helper (rest l) (add1 acc))]))])
    (count-helper lot-rev 0)))

;; LoTree --> LoTree
(define (update-all-scenics lotree)
  (cond [(empty? lotree) '()]
        [(cons?  lotree) (cons
                          (tree (tree-height (last lotree))
                                (tree-vis (last lotree))
                                (* (tree-scenic (last lotree)) (calc-scenic lotree)))
                          (update-all-scenics (reverse (rest (reverse lotree)))))]))

;; Forest --> Forest
(define (update-scenics f)
  (map (compose reverse update-all-scenics) f))

;; String --> Num
(define (max-scenic s)
  (let ([f (rotate-reduce (build-forest s) update-scenics)])
    (apply max (map (λ(l) (apply max (map tree-scenic l))) f))))


