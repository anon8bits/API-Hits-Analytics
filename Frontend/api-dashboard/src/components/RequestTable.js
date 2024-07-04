import React, { useState, useEffect } from 'react';
import { fetchRequestHistory } from '../services/fetchData';
import styles from './css/RequestTable.module.css';

const RequestTable = () => {
    const [requests, setRequests] = useState([]);
    const [days, setDays] = useState(30);
    const [currentPage, setCurrentPage] = useState(1);
    const [searchTerm, setSearchTerm] = useState('');
    const itemsPerPage = 10;

    useEffect(() => {
        const loadRequests = async () => {
            try {
                const data = await fetchRequestHistory(days);
                setRequests(data);
                setCurrentPage(1);
            } catch (error) {
                console.error("Error fetching request history:", error);
            }
        };

        loadRequests();
    }, [days]);

    const handleDaysChange = (event) => {
        setDays(Number(event.target.value));
    };

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
        setCurrentPage(1);
    };

    const filteredRequests = requests.filter(request =>
        Object.values(request).some(value =>
            value.toString().toLowerCase().includes(searchTerm.toLowerCase())
        )
    );

    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = filteredRequests.slice(indexOfFirstItem, indexOfLastItem);

    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    return (
        <div className={styles.tableContainer}>
            <div className={styles.tableHeader}>
                <h2>Requests</h2>
                <div className={styles.tableControls}>
                    <input
                        type="text"
                        placeholder="Search"
                        value={searchTerm}
                        onChange={handleSearchChange}
                        className={styles.searchInput}
                    />
                    <select value={days} onChange={handleDaysChange} className={styles.daysSelect}>
                        <option value={1}>Last 1 day</option>
                        <option value={7}>Last 7 days</option>
                        <option value={15}>Last 15 days</option>
                        <option value={30}>Last 30 days</option>
                    </select>
                </div>
            </div>
            <table className={styles.requestTable}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Req. Status</th>
                        <th>Req. Type</th>
                        <th>Req. Time</th>
                        <th>Content Type</th>
                        <th>IP Address</th>
                        <th>OS</th>
                        <th>User Agent</th>
                    </tr>
                </thead>
                <tbody>
                    {currentItems.map((request, index) => (
                        <tr key={request.id}>
                            <td>{request.id}</td>
                            <td>{request.status_code}</td>
                            <td>{request.request_type}</td>
                            <td>{new Date(request.timestamp).toLocaleString()}</td>
                            <td>Application/JSON</td>
                            <td>{request.ip_address}</td>
                            <td>{request.os}</td>
                            <td>{request.user_agent}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className={styles.pagination}>
                {Array.from({ length: Math.ceil(filteredRequests.length / itemsPerPage) }, (_, i) => (
                    <button key={i} onClick={() => paginate(i + 1)} className={currentPage === i + 1 ? styles.activePage : ''}>
                        {i + 1}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default RequestTable;