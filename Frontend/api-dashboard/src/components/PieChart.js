import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { fetchColumnAggregate } from '../services/fetchData';
import styles from './css/PieChart.module.css';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const BrowserPieChart = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const loadData = async () => {
            try {
                const result = await fetchColumnAggregate('user_agent');
                const total = result.reduce((sum, item) => sum + item.count, 0);
                const dataWithPercentage = result.map(item => ({
                    ...item,
                    percentage: ((item.count / total) * 100).toFixed(1)
                }));
                setData(dataWithPercentage);
            } catch (error) {
                console.error("Error fetching browser data:", error);
            }
        };

        loadData();
    }, []);

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            return (
                <div className={styles.customTooltip}>
                    <p>{`${data.label}: ${data.percentage}%`}</p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className={styles.pieContainer}>
            <div className={styles.header}>
                <h2>Browser</h2>
                <p>No of requests by browser</p>
            </div>
            <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                    <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="count"
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                </PieChart>
            </ResponsiveContainer>
            <div className={styles.legend}>
                {data.map((entry, index) => (
                    <div key={`legend-${index}`} className={styles.legendItem}>
                        <span style={{ backgroundColor: COLORS[index % COLORS.length] }}></span>
                        {entry.label}: {entry.percentage}%
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BrowserPieChart;