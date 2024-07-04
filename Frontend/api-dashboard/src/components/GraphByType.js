import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { fetchColumnAggregate } from '../services/fetchData';
import styles from './css/ColumnGraph.module.css';

const ColumnGraph = () => {
    const [data, setData] = useState([]);
    const [column, setColumn] = useState('request_type');
    const columns = ['endpoint', 'os', 'request_type', 'status_code', 'user_agent'];

    useEffect(() => {
        const loadData = async () => {
            try {
                const result = await fetchColumnAggregate(column);
                setData(result);
            } catch (error) {
                console.error("Error fetching column data:", error);
            }
        };

        loadData();
    }, [column]);

    const handleColumnChange = (event) => {
        setColumn(event.target.value);
    };

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className={styles.customTooltip}>
                    <p>{`${payload[0].payload.label}: ${payload[0].value}`}</p>
                </div>
            );
        }
        return null;
    };

    const CustomXAxisTick = ({ x, y, payload }) => {
        return (
            <g transform={`translate(${x},${y})`}>
                <text
                    x={0}
                    y={0}
                    dy={16}
                    textAnchor="end"
                    fill="#666"
                    transform="rotate(-90)"
                    style={{ fontSize: '12px' }}
                >
                    {payload.value}
                </text>
            </g>
        );
    };

    return (
        <div className={styles.graphContainer}>
            <div className={styles.header}>
                <h2>Request Type</h2>
                <p>Number of requests based on type</p>
                <select value={column} onChange={handleColumnChange} className={styles.dropdown}>
                    {columns.map((col) => (
                        <option key={col} value={col}>
                            {col.replace('_', ' ').charAt(0).toUpperCase() + col.replace('_', ' ').slice(1)}
                        </option>
                    ))}
                </select>
            </div>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 100 }}>
                    <XAxis
                        dataKey="label"
                        axisLine={false}
                        tickLine={false}
                        interval={0}
                        height={100}
                        tick={<CustomXAxisTick />}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="count" fill="#8884d8">
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={`hsl(${index * 60}, 70%, 60%)`} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};

export default ColumnGraph;