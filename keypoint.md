# Key Point
## visualization
Did you know keras provides a [tool](https://keras.io/visualization/) to generate a diagram of the model for better visualization?

```python
from keras.utils import plot_model
plot_model(model, to_file='model.png')
```
OR
```python
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

SVG(model_to_dot(model).create(prog='dot', format='svg'))
```
