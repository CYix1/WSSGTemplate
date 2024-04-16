using UnityEngine;

/*
 * Basic SingletonWrapper
 */
public class SingletonPersistant<T> : MonoBehaviour where T : MonoBehaviour
{
    public static T Instance;

    [Header("Singleton")] [SerializeField] private bool dontDestroyOnLoad = true;

    protected void Awake()
    {
        if (Instance == null)
        {
            Instance = this as T;

            GameObject go;
            (go = gameObject).transform.SetParent(null);
            if (dontDestroyOnLoad)
                DontDestroyOnLoad(go);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    private void OnDestroy()
    {
        if (Instance == this)
            Instance = null;
    }
}