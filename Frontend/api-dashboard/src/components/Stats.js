import React, { useState, useEffect } from 'react';
import { fetchStats } from '../services/fetchData';
import styles from './css/Stats.module.css';

const Stats = () => {
    const [stats, setStats] = useState({
        total_requests: 0,
        average_response_time: 0,
        failed_requests: 0
    });

    useEffect(() => {
        const loadStats = async () => {
            try {
                const data = await fetchStats();
                setStats(data);
            } catch (error) {
                console.error("Error fetching stats:", error);
            }
        };

        loadStats();
    }, []);

    return (
        <div className={styles.statsContainer}>
            <div className={styles.card}>
                <StatItem
                    icon="💰"
                    value={stats.total_requests.toLocaleString()}
                    label="Total Request"
                    color="#4caf50"
                />
                <StatItem
                    icon="⏱️"
                    value={`${(stats.average_response_time * 1000).toFixed(1)}ms`}
                    label="Avg. Response Time"
                    color="#2196f3"
                />
                <StatItem
                    icon="🛍️"
                    value={stats.failed_requests}
                    label="Failed Requests"
                    color="#e91e63"
                />
            </div>
        </div>
    );
}

const StatItem = ({ icon, value, label, color }) => (
    <div className={styles.statItem}>
        <div className={styles.icon} style={{ backgroundColor: color }}>
            {icon}
        </div>
        <div className={styles.details}>
            <div className={styles.label}>{label}</div>
            <div className={styles.value}>{value}</div>
        </div>
    </div>
);

export default Stats;