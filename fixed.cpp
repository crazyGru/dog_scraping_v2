template <class T> 
class Array { 
private:   
    T *m_pData;   
    unsigned int m_nSize; 
public:  
    Array(unsigned int nSize=0) : m_nSize(nSize) {
        if (m_nSize > 0)   
            m_pData = new (std::nothrow) T[m_nSize](); // Initialize memory with default values
        else
            m_pData = nullptr; // Handle case when nSize is 0
    } 
    virtual ~Array() {
        if (m_pData != nullptr)
            delete[] m_pData; // Use delete[] for arrays
    }
    bool Set(unsigned int nPos, const T& Value) {
        if (nPos < m_nSize) {
            m_pData[nPos] = Value;
            return true;
        } 
        else {
            return false;
        }
    } 
    T Get(unsigned int nPos) {
        if (nPos < m_nSize)
            return m_pData[nPos];
        else
            return T();
    } 
};
/*
Bug1: Memory Leak
Test Case:
    Array<int>* arr = new Array<int>(5);
    delete arr;
*/
/*
Bug2: Incorrect Deletion 
Test Case:
    Array<int> arr(5);
    arr.Set(0, 10);
    arr.Set(1, 20);
    arr.Set(2, 30);
    arr.Set(3, 40);
    arr.Set(4, 50);
*/
/*
Bug3: Out of Bounds Access 
Test Case:
    Array<int> arr(5);
    arr.Set(0, 10);
    arr.Set(1, 20);
    arr.Set(2, 30);
    arr.Set(3, 40);
    arr.Set(4, 50);
    int value = arr.Get(5);
*/