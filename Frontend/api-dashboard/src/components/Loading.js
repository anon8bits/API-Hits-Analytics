import React from 'react';
import styles from './css/Loading.module.css'

const Loading = () => {
  return (
    <>
      <div className={styles.loadingContainer}>
        <button className={styles.loaderBtn}>
          <div className={styles.loader}></div>
          Loading ...
        </button>
      </div>
    </>
  );
};

export default Loading;
