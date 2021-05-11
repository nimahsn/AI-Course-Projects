import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras import backend as K


def deep_auto_recommender_model(input_matrix, units, activation_fn, output_activation, latent_dropout=0,
                                input_drop_out=0, batch_normalization=True):
    x = input_layer = keras.layers.Input(shape=input_matrix.shape[1], name="input_layer")
    if input_drop_out > 0:
        x = keras.layers.Dropout(rate=input_drop_out)(x)
    if batch_normalization:
        x = keras.layers.BatchNormalization()(x)

    for i in range(0, len(units) // 2):
        x = keras.layers.Dense(units[i], name="encoder_{}".format(i + 1),
                               kernel_regularizer=keras.regularizers.l2(0.001))(x)
        x = keras.activations.get(activation_fn)(x)
        if latent_dropout > 0:
            # x = keras.layers.Dropout(latent_dropout)(x)
            pass
        if batch_normalization:
            x = keras.layers.BatchNormalization()(x)

    x = keras.layers.Dense(units=units[len(units) // 2], name="latent",
                           kernel_regularizer=keras.regularizers.l2(0.001))(x)
    x = keras.activations.get(activation_fn)(x)
    if latent_dropout > 0:
        x = keras.layers.Dropout(latent_dropout)(x)
        # pass
    if batch_normalization:
        x = keras.layers.BatchNormalization()(x)

    for i in range((len(units) // 2) + 1, len(units)):
        x = keras.layers.Dense(units[i], name="decoder_{}".format(i - len(units) // 2),
                               kernel_regularizer=keras.regularizers.l2(0.001))(x)
        x = keras.activations.get(activation_fn)(x)
        if latent_dropout > 0:
            # x = keras.layers.Dropout(latent_dropout)(x)
            pass
        if batch_normalization:
            x = keras.layers.BatchNormalization()(x)

    output_layer = keras.layers.Dense(input_matrix.shape[1], activation=output_activation,
                                      kernel_regularizer=keras.regularizers.l2(0.001), name="predictions")(x)

    return keras.Model(input_layer, output_layer)


def masked_mse(y_true, y_pred):
    # masked function
    mask_true = K.cast(K.not_equal(y_true, 0), K.floatx())
    # masked squared error
    masked_squared_error = K.square(mask_true * (y_true - y_pred))
    masked_mse_ = K.sum(masked_squared_error, axis=-1) / K.maximum(K.sum(mask_true, axis=-1), 1)
    return masked_mse_


def masked_rmse(y_true, y_pred):
    # masked function
    mask_true = K.cast(K.not_equal(y_true, 0), K.floatx())
    # masked squared error
    masked_squared_error = K.square(mask_true * (y_true - y_pred))
    masked_mse_ = K.sqrt(K.sum(masked_squared_error, axis=-1) / K.maximum(K.sum(mask_true, axis=-1), 1))
    return masked_mse_


def masked_rmse_clip(y_true, y_pred):
    # masked function
    mask_true = K.cast(K.not_equal(y_true, 0), K.floatx())
    y_pred = K.clip(y_pred, 1, 5)
    # masked squared error
    masked_squared_error = K.square(mask_true * (y_true - y_pred))
    masked_mse_ = K.sqrt(K.sum(masked_squared_error, axis=-1) / K.maximum(K.sum(mask_true, axis=-1), 1))
    return masked_mse_
