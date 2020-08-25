def ucb1_policy(df, t, ucb_scale=2.0):
    '''
    Applies UCB1 policy to generate movie recommendations
    Args:
        df: dataframe. Dataset to apply UCB policy to.
        ucb_scale: float. Most implementations use 2.0.
        t: int. represents the current time step.
    '''
    scores = df[['movieId', 'liked']].groupby('movieId').agg({'liked': ['mean', 'count', 'std']})
    scores.columns = ['mean', 'count', 'std']
    scores['ucb'] = scores['mean'] + np.sqrt(
            (
                (2 * np.log10(t)) /
                scores['count']
            )
        )
    scores['movieId'] = scores.index
    scores = scores.sort_values('ucb', ascending=False)
    recs = scores.loc[scores.index[0:args.n], 'movieId'].values
    return recs

recs = ucb1_policy(df=history.loc[history.t<=t,], t, ucb_scale=args.ucb_scale)
history, action_score = score(history, df, t, args.batch_size, recs)




train = sqlContext.load(source="com.databricks.spark.csv", path = 'PATH/train.csv', header = True,inferSchema = True)
test = sqlContext.load(source="com.databricks.spark.csv", path = 'PATH/test-comb.csv', header = True,inferSchema = True)