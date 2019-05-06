## Scraping pdf files using pdfquery
Pdf files can be converted to xml and be queried using pdfquery. It supports both xpath using the underlying and css 
selector like syntax. 

To get the required data from the pdf file, we can use any of the following 3 methods.

#### Method 1 - Bounding Box:
Bounding box method can be used when the required text always lies in the same area of the page in every page

__Parameters:__ 
- (x0, y0, x1, y1) : The coordinates of the bounding box

#### Method 2 - Adjacent Element:
Using the generated XML we can get adjacent element to the label element. But this only works when the text is in the 
adjacent element to the element containing the label. The problem is that there are times when big spaces and 
unrecognized characters seem to break the text into multiple elements.Also multiple lines of texts happen to be in 
multiple elements.

__Parameters:__
- label text : The text contained in the label.

#### Method 3 - Adjacent Bounding Box:
Combining the methods 2 and 1, we can first find the position of the element using it's label and use the position of 
the label to find a bounding box large enough to bound the required text.

__Parameters:__
- label text :  The text contained in the label.
- position : Top, Right, Bottom or Left, The position of the text relative to the label
- distance : Distance from the label to the text
- width : width of the text 
- height  : height of the text

Method 3 seems to be the most effective method as most of the text data we require seem to have labels.
But there are also time when method 1 is useful, as it is easier to use. Though it mostly only works when the label
and the text are in the same line and the text is in a single line.

For complex cases a customized version of method 3 can be used.

#### References:

- pdfquery repository: https://github.com/jcushman/pdfquery


