# Computer Vision (Recurrent Neural Network)

## Ziel
Ziel dieses Projektes ist es ein RNN zu trainieren, sodass es einen Gegenstand (z.B. einen Ball) in einem Video Tracken kann.

## Vorgehen
Für das überwachte Training des RNN haben wir zunächst [Videos](./Videos) erzeugt und diese anschließend [annotiert](./Annotations)
Die Annotations beschreiben die Position (und Bounding Boxen) der Bälle in den Videos für jedes Frame.

### Annotations
Die Annotations JSON-Files mit einem Array aus `Frames`

#### Frame
```JSON
{
	"frameNumber": INT,
	"balls": 
	[
		BALL,
		BALL,
		...
	]
}
```  

#### Ball
`tag` wird genutzt um mehrere Bälle im verlauf eines Videos auseinander halten zu können.
Der erste ball bekommt als tag eine `1`, der zweite eine `2`, der dritte eine `3` usw...
`position` beschreibt den Mittelpunkt des Balles (und der Bounding Box).
`boundingBox` beschreibt die ausmaße (Höhe und Breite) des Balles im Frame.
```JSON
{
	"tag": INT,
	"position": POINT,
	"boundingBox": BOX
}
```  

#### Point
```JSON
{
	"x": INT,
	"y": INT
}
```  

#### BOX
```JSON
{
	"width": INT,
	"height": INT
}
```  

## Links

[Slack](https://computer-vision-rnn.slack.com)

[Trello](https://trello.com/b/XAJalI7K/rnn-computer-vision)

### Linksammlung allgemein
https://www.quora.com/Why-is-no-visual-tracking-algorithm-using-RNN-LSTM - Interessante Artikelsammlung über RNN/Object Tracking

http://www.wildml.com/2015/09/recurrent-neural-networks-tutorial-part-1-introduction-to-rnns/ - How To RNN selber schreiben
