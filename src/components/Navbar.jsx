import styles from './Navbar.module.css';

export default function Navbar() {
  return (
    <nav>
      <div className={styles.navLeft}>
        <button>⚙️</button>
      </div>
      <div className={styles.navCenter}>
        <button>🔍</button>
        <p>Type to GAIA</p>
      </div>
      <div className={styles.navRight}>
        <button>👤</button>
      </div>
    </nav>
  );
}
