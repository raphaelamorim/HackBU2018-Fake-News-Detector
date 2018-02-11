from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import tensorflow as tf

import news_data

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=50, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')

def main(argv):
    args = parser.parse_args(argv[1:])

    # Fetch the data
    (train_features, train_label), (test_features, test_label) = news_data.load_data()

    # Feature columns describe how to use the input.
    my_feature_columns = []
    for key in train_features.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))

    # Build 2 hidden layer DNN with 7, 7 units respectively.
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        # Two hidden layers of 7 nodes each.
        hidden_units=[7, 7],
        # The model must choose between 2 classes.
        n_classes=2)

    # Train the Model.
    classifier.train(input_fn=lambda:news_data.train_input_fn(
					train_features, train_label, args.batch_size),
					steps=args.train_steps)

    # Evaluate the model.
    eval_result = classifier.evaluate(
        input_fn=lambda:news_data_data.eval_input_fn(test_features, test_label,
                                                args.batch_size))

    print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    # Generate predictions from the model
    expected = ['Fake', 'Real', 'Fake']
    predict_features = {
        'FleschReading': [5.1, 5.9, 6.9],
        'FleschKincaid': [3.3, 3.0, 3.1],
        'ColemanLiau': [1.7, 4.2, 5.4],
        'Typo': [0.5, 1.5, 2.1],
        'DiffWord': [1.7, 4.2, 5.4],
        'PartsOfSpeech': [0.5, 1.5, 2.1],
        'GoogleResults': [1.7, 4.2, 5.4],
        'WhoIs': [0.5, 1.5, 2.1]
    }

    predictions = classifier.predict(
        input_fn=lambda:iris_data.eval_input_fn(predict_features,
                                                labels=None,
                                                batch_size=args.batch_size))

    for pred_dict, expec in zip(predictions, expected):
        template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')

        class_id = pred_dict['class_ids'][0]
        probability = pred_dict['probabilities'][class_id]

        print(template.format(news_data.SPECIES[class_id],
                              100 * probability, expec))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)
