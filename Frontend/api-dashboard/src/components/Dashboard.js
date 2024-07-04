import React from 'react';
import Stats from './Stats';
import ColumnGraph from './GraphByType';
import BrowserPieChart from './PieChart';
import styles from './css/Dashboard.module.css';
import RequestTable from './RequestTable';

const Dashboard = () => {
  return (
    <div className={styles.dashboard}>
      <Stats />
      <div className={styles.graphRow}>
        <ColumnGraph />
        <BrowserPieChart />
      </div>
      <RequestTable />
    </div>
  );
};

export default Dashboard;